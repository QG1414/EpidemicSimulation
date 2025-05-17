import json
from generationScripts.generation import *
from generationScripts.pathsGenerator import PathsGeneratorCalculus, PathsGeneratorVisual
from enums.presetEnums import *
from enums.epidemyEnums import *
from matplotlib.animation import FuncAnimation
import cupy as cp
from kivy.clock import Clock
import time
from helper import resource_path

class SymulationPreData:

    base_chance_to_meet : dict[int, float]
    chance_to_meet : dict[int, float]
    n : int
    k : int
    p : int

    def __init__( self, chance_to_meet : dict[int, float], n : int, k : int, p : int ) -> None:
        self.chance_to_meet = chance_to_meet
        self.base_chance_to_meet = chance_to_meet.copy()
        self.n = n
        self.k = k
        self.p = p
        

class SymulationData:

    preset_path : str = ""

    #region init

    def __init__( self, gd : GenerationData, spd : SymulationPreData, modif : dict[str, any], enable_cuda : bool = False, symulation_name : str = "", use_log : bool = True , use_animation : bool = True , current_preset_name : str = PRESETS_NAMES.NONE.value ) -> None:
        self.__set_all_data( gd, spd, modif, enable_cuda, symulation_name, use_log, use_animation, current_preset_name )
    
    def __set_all_data( self, gd : GenerationData, spd : SymulationPreData, modif : dict[str, any], enable_cuda : bool = False, symulation_name : str = "", use_log : bool = True , use_animation : bool = True , current_preset_name : str = PRESETS_NAMES.NONE.value ) -> None:
        self.gd : GenerationData = gd
        self.spd : SymulationPreData = spd
        self.use_log : bool = use_log
        self.use_animation : bool = use_animation
        self.modif : dict[str, any] = modif
        self.enable_cuda : bool = enable_cuda
        self.symulation_name : str = symulation_name
        self.force_cancel_var : bool = False
        self.current_preset : str = current_preset_name
        self.set_cuda( enable_cuda )

        self.path_generator : PathsGeneratorCalculus = PathsGeneratorCalculus(spd.k, spd.p, spd.chance_to_meet, gd, self.enable_cuda, **modif)
        self.path_generator_visual : PathsGeneratorVisual = PathsGeneratorVisual(spd.n,spd.k, symulation_name )

        self.return_data : list[any] = [
            self.gd.generation_size, 
            self.gd.curing_time_min,
            self.gd.curing_time_max,
            self.gd.base_curing_prob,
            self.gd.resTime_min,
            self.gd.resTime_max,
            self.spd.base_chance_to_meet,
            self.spd.n,
            self.spd.k,
            self.spd.p,
        ]

    #endregion init

    #region import_preset

    def import_preset_not_static( self, import_path : str, preset_name : str ) -> any:
        cuda_available = cp.cuda.runtime.getDeviceCount() > 0

        if self.enable_cuda and cuda_available != self.enable_cuda:
            print( "ERROR! Cuda isn't detected on device so it was autamaticly disabled" ) 

        self.enable_cuda = self.enable_cuda if cuda_available else False

        Generation_params : list[any] = [ GenerationSubPresets, CuringSubPresets, ResistanceSubPresets ]
        Additional_params : list[any] = [ SymulationSubPresets, EpidemySubPresets ]

        self.preset_path = import_path

        if self.enable_cuda:
            import_path = PRESETS_BASE.GPU.value + import_path
        else:
            import_path = PRESETS_BASE.CPU.value + import_path
        
        final_path = resource_path(import_path)

        with open(final_path, encoding="utf-8") as f:
            d : dict = json.load(f)
            name : str = "Simulating preset: " + f"$\\bf{{{d[MainPresets.NAME.value].replace(' ', '\ ')}}}$"
            generation : GenerationData = self.__import_general_params(Generation_params, [d.get(MainPresets.GENERATION.value), d.get(MainPresets.CURING.value), d.get(MainPresets.RESISTANCE.value)])
            additional_data : SymulationPreData = self.__import_additional_params(Additional_params, [d.get(MainPresets.SYMULATION.value), d.get(MainPresets.EPIDEMY.value)])
            modifiers_data : list[any] = self.__import_modifiers_params([d.get(MainPresets.MODIFIERS.value), d.get(MainPresets.VACCINES.value)])
            self.__set_all_data(generation, additional_data, modifiers_data, self.enable_cuda, name, self.use_log, self.use_animation, preset_name)

    def __import_general_params( self, params : list[any], dict_values : list[dict[str:any]] ) -> GenerationData:
        generation_params : list[any] = []
        for index,param in enumerate(params):
            for i in param:
                generation_params.append(dict_values[index].get(i.value))
        new_generation = GenerationData(
            generation_params[0], generation_params[1], generation_params[2], 
            generation_params[3], generation_params[4], generation_params[5], 
            generation_params[6]
            )
        return new_generation

    def __import_additional_params( self, params : list[any], dict_values : list[dict[str:any]] ) -> SymulationPreData:
        additional_params : list[any] = []
        for index,param in enumerate(params):
            for i in param:
                data = dict_values[index].get(i.value)
                if i == SymulationSubPresets.MEETING_CHANCE:
                    data = {int(k) : v for k,v in data.items()}
                additional_params.append(data)
        return SymulationPreData(*additional_params)

    def __import_modifiers_params( self, dict_values : list[dict[str:any]] ) -> dict[str,any]:
        vaccines_params : dict[VACCINES_PARAMS:any] = {
            VACCINES_PARAMS.POPULATION_VACCINATED : 0, 
            VACCINES_PARAMS.DAY_OF_VACCINES : 0 
        } 

        modif : dict[str,any] = {
            MODIFIERS.HYGIENE.value : MODIF_LEVELS.NORMAL,
            MODIFIERS.POPULATION_CONTROL.value : MODIF_LEVELS.NORMAL,
            MODIFIERS.HEALTHCARE.value : MODIF_LEVELS.NORMAL,
            MODIFIERS.VACCINES.value : MODIF_ENABLED.DISABLED,
            VACCINES_PARAMS.VACCINES_PARAM.value : vaccines_params
        }

        modif_list : list[any] = [MODIFIERS.HYGIENE.value, MODIFIERS.POPULATION_CONTROL.value, MODIFIERS.HEALTHCARE.value, MODIFIERS.VACCINES.value ]
        modif_levels : list[MODIF_LEVELS] = [MODIF_LEVELS.VERY_BAD, MODIF_LEVELS.BAD, MODIF_LEVELS.NORMAL, MODIF_LEVELS.GOOD, MODIF_LEVELS.VERY_GOOD ]

        for index, val in enumerate(ModifiersSubPresets):
            data_value = dict_values[0].get(val.value)
            if not isinstance( data_value, bool ):
                modif[modif_list[index]] = modif_levels[data_value]
            else:
                modif[modif_list[index]] = MODIF_ENABLED.ENABLED if data_value else MODIF_ENABLED.DISABLED
        
        if not modif[MODIFIERS.VACCINES.value]:
            return modif
        
        vaccines_params[VACCINES_PARAMS.POPULATION_VACCINATED] = dict_values[1].get(VaccinesSubPresets.POPULATION.value)
        vaccines_params[VACCINES_PARAMS.DAY_OF_VACCINES] = dict_values[1].get(VaccinesSubPresets.DAY.value)
        
        return modif
    
    #endregion import_preset


#region getters

    def get_current_data( self ) -> tuple[list[any], dict[str,any]]:
        return (self.return_data, self.modif)
    
    def get_vaccines_params( self, name : VACCINES_PARAMS ) -> int | float:
        return self.modif.get(VACCINES_PARAMS.VACCINES_PARAM.value).get(name)
    
#endregion getters


#region setters

    def update_all_data( self, gd : GenerationData, spd : SymulationPreData, modifs : list[MODIF_LEVELS], vaccines_enabled : bool, vaccines_params : list[any]  ) -> None:
        self.current_preset = PRESETS_NAMES.NONE.value
        self.symulation_name = ""
        final_modifs = self.generate_modif( modifs, vaccines_enabled, vaccines_params )
        self.__set_all_data( gd, spd, final_modifs, self.enable_cuda, self.symulation_name, self.use_log, self.use_animation, self.current_preset )
    
    def generate_modif( self, modif : list[MODIF_LEVELS], vaccines_enabled : bool, vaccines_params : list[any] ) -> dict[any]:
        final_modif = {}
        keys = [MODIFIERS.HYGIENE.value, MODIFIERS.POPULATION_CONTROL.value, MODIFIERS.HEALTHCARE.value]
        for index, key in enumerate( keys ):
            final_modif[key] = modif[index]

        return {**final_modif, **self.generate_vaccines_modif(vaccines_enabled, vaccines_params)}

    def generate_vaccines_modif( self, vaccines_enabled : bool, vaccines_params : list[any] ) -> dict[any]:
        vacc_modif = {MODIFIERS.VACCINES.value : (MODIF_ENABLED.ENABLED if vaccines_enabled else MODIF_ENABLED.DISABLED) }
        vacc_params = {VACCINES_PARAMS.POPULATION_VACCINATED : 0, VACCINES_PARAMS.DAY_OF_VACCINES : 0}

        if vaccines_enabled:
            for index, key in enumerate(vacc_params.keys()):
                vacc_params[key] = vaccines_params[index]
        
        vacc_modif.setdefault(VACCINES_PARAMS.VACCINES_PARAM.value, vacc_params)
        return vacc_modif
    
    def set_cuda( self, enable_cuda : bool, update_preset : bool = False ) -> bool:
        self.enable_cuda = enable_cuda
        cuda_available = cp.cuda.runtime.getDeviceCount() > 0

        if enable_cuda and (enable_cuda != cuda_available or not self.is_cuda_usable()):
            print( "ERROR! Cuda isn't detected on device so it was autamaticly disabled" ) 
            self.enable_cuda = False
        
        if update_preset and self.current_preset != PRESETS_NAMES.NONE.value:
            self.import_preset_not_static( self.preset_path, self.current_preset )
        
        return enable_cuda == self.enable_cuda


    def is_cuda_usable( self ) -> bool:
        try:
            test_array = cp.array([1,2,3])
            result = cp.cumsum(test_array)
            _ = result.get()
            return True
        except cp.cuda.runtime.CUDARuntimeError as e:
            print( f"CUDA runtime error: {e}" )
            return False
        except Exception as e:
            print( f"Unexpected error when checking CUDA: {e}" )
            return False 

#endregion setters


#region load_data

    def start_load_data( self, visuals ) -> None:
        time.sleep(0.1)
        self.visuals = visuals
        self.__generate_lines()

        if self.force_cancel_var:
            self.force_cancel_var = False
            self.path_generator.force_cancel = False
            Clock.schedule_once(lambda dt: self.visuals.back_to_main(), 0)
            return

        Clock.schedule_once(lambda dt: self.visuals.after_loading(), 0)
        time.sleep(0.1)
        Clock.schedule_once(lambda dt: self.visuals.finish_loading(), 0)
    

    def __generate_lines( self ) -> None:
        self.lines_data : list[Generation] = self.path_generator.generate_paths(self.spd.n, self.visuals)

        if self.force_cancel_var:
            return None

        self.y_min = float("inf")
        self.y_max = float("-inf")
        for i in self.lines_data:
            self.y_min = min( self.y_min, min( i.path_positions[1] ) )
            self.y_max = max( self.y_max, max( i.path_positions[1] ) )
    
#endregion load_data


#region restart_data


    def force_cancel( self ) -> None:
        self.force_cancel_var = True
        self.path_generator.force_cancel = True
    
    def restart_data( self ) -> None:
        self.path_generator.reset_data( self.enable_cuda )

    def restart_plot( self ) -> None:
        self.path_generator_visual.restart_plot( self.symulation_name )
        self.__set_scale()
    
    def __set_scale( self ) -> None:
        self.path_generator_visual.set_scale(self.y_min, self.y_max, log = self.use_log)

#endregion restart_data


    def start_graphing( self , animate : bool = True ) -> FuncAnimation:
        self.restart_plot()
        return self.path_generator_visual.start_graphing(self.lines_data, animate=animate)
