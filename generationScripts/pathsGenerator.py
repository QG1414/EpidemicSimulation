import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from generationScripts.generation import Generation, GenerationData
from enums.epidemyEnums import *
import cupy as cp


class PathsGeneratorCalculus:

    #region init

    def __init__( self, k : int, p : int, population : dict[int:float], created_generation : GenerationData, enable_cuda : bool = False, **kwargs ) -> None:
        self.k : int = k
        self.p : int = p
        self.generated : int = 0
        self.population : dict[int:float] = population
        self.population_keys : np.ndarray[int] = np.array(list(population.keys()))
        self.population_probabilities : np.ndarray[float] = np.array(list(population.values()))
        self.created_generation : GenerationData = created_generation
        self.__update_modifiers(**kwargs)
        self.force_cancel = False
        self.reset_data( enable_cuda )

    def reset_data( self, enable_cuda ):
        self.enable_cuda : bool = enable_cuda
        self.generations : list[Generation] = []
        for _ in range(self.k):
            self.generations.append( Generation( self.created_generation ) )
    
    def __update_modifiers( self, **kwargs ) -> None:
        hygiene_level : MODIF_LEVELS = kwargs.get(MODIFIERS.HYGIENE.value, MODIF_LEVELS.NORMAL)
        self.p = min( self.p * hygiene_level.value, 1 )

        population_level : MODIF_LEVELS = kwargs.get(MODIFIERS.POPULATION_CONTROL.value, MODIF_LEVELS.NORMAL)
        self.__update_population(population_level.value)

        healthcare_level : MODIF_LEVELS = kwargs.get(MODIFIERS.HEALTHCARE.value, MODIF_LEVELS.NORMAL)
        self.created_generation.curing_prob = min( self.created_generation.curing_prob * (-healthcare_level.value + 2) , 1 )
        
        vaccines_created : MODIF_ENABLED = kwargs.get(MODIFIERS.VACCINES.value, MODIF_ENABLED.DISABLED)
        if vaccines_created.value:
            vaccines_params : dict[VACCINES_PARAMS : any] = kwargs.get(VACCINES_PARAMS.VACCINES_PARAM.value, None)
            self.created_generation.add_vaccines(vaccines_params.get(VACCINES_PARAMS.POPULATION_VACCINATED, 0), vaccines_params.get(VACCINES_PARAMS.DAY_OF_VACCINES, 0))

    def __update_population( self, value_to_update : float ) -> None:
        found_min = -1
        sum_value = 0
        for key, val in reversed( self.population.items() ):
            if found_min != -1:
                sum_value += val
                continue

            if np.isclose(val, 0):
                continue
            self.population[key] = min( self.population[key] * value_to_update, 1 )
            found_min = key

        max_val = 1 - self.population[found_min]

        for key, val in self.population.items():
            if key == found_min:
                break
            self.population[key] = ( self.population[key] / sum_value ) * max_val


    #endregion

    #region baches

    def get_safe_batch_size( self, reserved_mem = 300 * 1024 * 1024 ):
        try:
            free_mem, _ = cp.cuda.runtime.memGetInfo()
            usable_mem = max(0, free_mem - reserved_mem)
            estimated_bytes_per_item = 10
            batch_size = usable_mem // estimated_bytes_per_item
            return int( batch_size )
        except Exception:
            return 10000000

    #endregion baches

    
    #region pathGeneration

    def __random_sum( self, N: int, main_generation: int, generation_number: int ) -> int:
        if N <= 0 or self.generations[main_generation].vulnerable_population <= 0:
            self.generations[main_generation].update_timeline(generation_number, 0)
            return self.generations[main_generation].infecting_population

        xp = cp if self.enable_cuda else np
        rng = xp.random.default_rng()

        population_prob = self.population_probabilities
        if self.enable_cuda:
            population_prob = cp.asarray(population_prob)

        culm_probs = xp.cumsum(population_prob)
        population_keys = xp.array(self.population_keys)

        batch_size = self.get_safe_batch_size() if self.enable_cuda else 5_000_000

        total_sum = 0

        sum_type = xp.int8
        max_bit_values = int(N * self.population_keys[-1]).bit_length()

        if( max_bit_values >= 30 ):
            sum_type = xp.int64
        elif max_bit_values >= 14:
            sum_type = xp.int32
        elif max_bit_values >= 6:
            sum_type = xp.int16

        batch_start = 0

        while batch_start < N:
            if self.force_cancel:
                return None
            current_batch_size = min(batch_size, N - batch_start)

            while True:
                try:
                    random_values = rng.random(current_batch_size)
                    indices = xp.searchsorted(culm_probs, random_values, side='right')
                    batch_population = population_keys[indices]

                    batch_binomial = (rng.random(current_batch_size) < self.p).astype(xp.int8)
                    batch_result = xp.sum( batch_binomial * batch_population, dtype=sum_type )

                    total_sum += batch_result
                    break
                except cp.cuda.memory.OutOfMemoryError:
                    current_batch_size = current_batch_size // 2
                    if current_batch_size < 1_000_000:
                        raise RuntimeError( "Not enough GPU memory even for smallest batch!" )
                    cp._default_memory_pool.free_all_blocks()

            batch_start += current_batch_size


        if self.enable_cuda:
            total_sum = total_sum.get()
            cp._default_memory_pool.free_all_blocks()
                    
        self.generations[main_generation].add_infection_info(generation_number, total_sum)
        return self.generations[main_generation].infecting_population

    def __random_path( self, n:int, main_generation:int ) -> tuple[int, int]:
        x = [0]
        y = [1]

        tmp_Z = 1

        for i in range(1, n+1):
            tmp_Z = self.__random_sum(tmp_Z, main_generation, i)
            if self.force_cancel:
                return None
            x.append(i)
            y.append(tmp_Z)
        return x, y

    def generate_paths( self, n:int, visuals ) -> list[Generation]:
        print(f"start generating simulations")
        for i in range(self.k):
            self.generations[i].add_path(self.__random_path(n,i))
            if self.force_cancel:
                return None
            print(f"symulation {i+1} / {self.k} finished")
            visuals.update_visuals(i+1)

        return self.generations
    
    #endregion pathGeneration
    

class PathsGeneratorVisual:

    #region Init

    def __init__( self, n:int, k:int, preset_name: str = "" ) -> None:
        self.ani = None
        self.preset_name : str = preset_name
        self.__set_calculus_vars( n, k )
    
    def __set_calculus_vars( self, n : int, k : int ) -> None:
        self.n : int = n
        self.k : int = k
    
    def __create_visual_vars( self ) -> None:
        self.fig : Figure
        self.ax : list[Axes]
        self.fig , self.ax = plt.subplots(ncols=2, figsize=(12, 6))
        self.fig.patch.set_facecolor('xkcd:mint green')

    def __base_visuals( self ) -> None:
        self.lines : list[list[Line2D]] = []
        for _ in range(self.k):
            line, = self.ax[0].plot([], [], lw=2)
            self.lines.append(line)
        self.pie_id : int = -1
        self.ax[1].pie([])

    #endregion Init

    #region hardVisuals

    def set_scale( self, min : int , max : int, additional_top_max : int = 20, linthresh : float = 0.5, log = False) -> None:
        self.ax[0].set_xlim(0, self.n)
        self.ax[0].set_ylim(min,max+additional_top_max)
        self.__set_scale_log(log, linthresh)

    def __set_scale_log( self, log : bool = True, linthresh : float = 0.5 ) -> None:
        if log:
            self.ax[0].set_yscale('symlog', linthresh=linthresh)
        else:
            self.ax[0].set_yscale("linear")

    #endregion hardVisuals

    #region pie_visuals

    def __calculate_pie_values( self, last_id : int, generations : list[Generation] ) -> None:
        if last_id == self.pie_id:
            return
        self.pie_id = last_id
        labels = {"epidemy" : 0, "stable" : 0, "ended" : 0}
        base_colors = {"epidemy" : "#e28d8d", "stable" : "#8669ff", "ended" : "#b2c085"}
        dead_population = 0
        gener : Generation
        for gener in generations:
            dead_population += gener.dead_population / gener.generation_size
            domin_state = gener.get_dominating_state()
            match( domin_state ):
                case EpidemyState.ENDED:
                    labels["ended"] += 1
                case EpidemyState.EPIDEMY:
                    labels["epidemy"] += 1
                case _:
                    labels["stable"] += 1
        labels = {i[0] : i[1] for i in labels.items() if i[1] > 0}
        colors = {}
        divider = len(generations) if len(generations) != 0 else 1

        for i in labels.keys():
            colors.setdefault(i, base_colors[i])

        self.__update_pie_visuals(labels, colors, ((dead_population / divider) * 100), last_id)



    def __update_pie_visuals( self, labels : dict[str,int], colors : dict[str:str], calculated_population : float, last_id : int ) -> None:        
        self.ax[1].clear()
        _, texts, _ = self.ax[1].pie(labels.values(), labels=labels.keys(), colors=colors.values(), autopct='%1.1f%%', pctdistance = 1.2, labeldistance = 0.6, rotatelabels =True, startangle=0, shadow=True, textprops = dict(rotation_mode = 'anchor', va='center'))
        for text in texts:
            text.set_fontsize(10)
        self.__update_symulation_number(calculated_population, last_id)
    
    def __update_symulation_number( self, calculated_population : float, last_id : int ) -> None:
        self.fig.texts.clear()
        self.fig.text(.01,.95,self.preset_name)
        self.fig.text(.7,.95,f"On average $\\bf{{{calculated_population:.4f}\\%}}$ of population is dead")
        self.fig.text(.125,.91,f"Current simulation: $\\bf{{{min(last_id + 1, self.k)} / {self.k}}}$")

    #endregion pie_visuals

    #region Animation

    def __init( self ) -> list[list[Line2D]]:
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def __update( self, frame : int, lines_data : list[Generation] ) -> list[list[Line2D]]:
        path_index = frame // self.n
        step = ( frame % self.n ) + 1

        for i, line in enumerate(self.lines):
            if i < path_index:
                x, y = lines_data[i].path_positions
                line.set_data(x, y)
            elif i == path_index:
                x, y = lines_data[i].path_positions
                line.set_data(x[:step], y[:step])
            else:
                line.set_data([], [])

        self.__calculate_pie_values(path_index, lines_data[:path_index])
        return self.lines
    
    #endregion Animation

    def restart_plot( self, symulation_name : str ):
        self.preset_name = symulation_name
        self.__create_visual_vars()
        self.__base_visuals()
        plt.axis("equal")

    def start_graphing( self, lines_data : list[Generation], animate : bool = True ) -> FuncAnimation | None:
        if animate:
            self.ani = FuncAnimation(
                self.fig,
                lambda frame : self.__update(frame, lines_data),
                frames=(self.n * self.k)+1,
                init_func= lambda : self.__init(),
                blit=False,
                interval=1,
                repeat=False
            )
        else:
            for i, line in enumerate(self.lines):
                line.set_data(lines_data[i].path_positions)
            self.__calculate_pie_values(self.k, lines_data)

        plt.show()
        return self.ani
    