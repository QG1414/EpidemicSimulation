import json
from generationScripts.generation import *
from generationScripts.pathsGenerator import PathsGeneratorCalculus, PathsGeneratorVisual
from enums.presetEnums import *
from enums.epidemyEnums import *
from matplotlib.animation import FuncAnimation
import cupy as cp

class SymulationData:

    #region init

    def __init__( self, gd : GenerationData, chance_to_meet : dict[int, int], n : int, k : int, p : int, modif : dict[str, any], enable_cuda : bool = False, symulation_name : str = "" ) -> None:
        self.gd : GenerationData = gd
        self.chance_to_meet_people : dict[int, int] = chance_to_meet
        self.n : int = n
        self.k : int = k
        self.p : float = p
        self.modif : dict[str, any] = modif

        cuda_available = cp.cuda.runtime.getDeviceCount() > 0
        if enable_cuda and enable_cuda != cuda_available:
            print( "ERROR! Cuda isn't detected on device so it was autamaticly disabled" ) 
            enable_cuda = False

        self.path_generator : PathsGeneratorCalculus = PathsGeneratorCalculus(k, p, chance_to_meet, gd, enable_cuda, **modif)
        self.path_generator_visual : PathsGeneratorVisual = PathsGeneratorVisual(n,k, symulation_name)

        self.__generate_lines()
        self.__set_scale()

    def __generate_lines( self ) -> None:
        self.lines_data : list[Generation] = self.path_generator.generate_paths(self.n)

        self.y_min = float("inf")
        self.y_max = float("-inf")
        for i in self.lines_data:
            self.y_min = min( self.y_min, min( i.path_positions[1] ) )
            self.y_max = max( self.y_max, max( i.path_positions[1] ) )
    
    def __set_scale( self ) -> None:
        self.path_generator_visual.set_scale(self.y_min, self.y_max)

    #endregion init

    #region import_preset

    @classmethod
    def import_preset( cls, import_path : str, enable_cuda : bool = False ) -> any:
        cuda_available = cp.cuda.runtime.getDeviceCount() > 0

        if enable_cuda and cuda_available != enable_cuda:
            print( "ERROR! Cuda isn't detected on device so it was autamaticly disabled" ) 

        enable_cuda = enable_cuda if cuda_available else False

        Generation_params : list[any] = [ GenerationSubPresets, CuringSubPresets, ResistanceSubPresets ]
        Additional_params : list[any] = [ SymulationSubPresets, EpidemySubPresets ]

        if enable_cuda:
            import_path = PRESETS_BASE.GPU.value + import_path
        else:
            import_path = PRESETS_BASE.CPU.value + import_path

        with open(import_path, encoding="utf-8") as f:
            d : dict = json.load(f)
            name : str = "Simulating preset: " + f"$\\bf{{{d[MainPresets.NAME.value].replace(' ', '\ ')}}}$"
            generation : GenerationData = cls.__import_general_params(Generation_params, [d.get(MainPresets.GENERATION.value), d.get(MainPresets.CURING.value), d.get(MainPresets.RESISTANCE.value)])
            additional_data : list[any] = cls.__import_additional_params(Additional_params, [d.get(MainPresets.SYMULATION.value), d.get(MainPresets.EPIDEMY.value)])
            modifiers_data : list[any] = cls.__import_modifiers_params([d.get(MainPresets.MODIFIERS.value), d.get(MainPresets.VACCINES.value)])
            return cls(generation, additional_data[0], additional_data[1], additional_data[2], additional_data[3], modifiers_data, enable_cuda, name)

    def __import_general_params( params : list[any], dict_values : list[dict[str:any]] ) -> GenerationData:
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

    def __import_additional_params( params : list[any], dict_values : list[dict[str:any]] ) -> list[any]:
        additional_params : list[any] = []
        for index,param in enumerate(params):
            for i in param:
                data = dict_values[index].get(i.value)
                if i == SymulationSubPresets.MEETING_CHANCE:
                    data = {int(k) : v for k,v in data.items()}
                additional_params.append(data)
        return additional_params

    def __import_modifiers_params( dict_values : list[dict[str:any]] ) -> dict[str,any]:
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

    def start_gaphing( self, animate : bool = True ) -> FuncAnimation:
        return self.path_generator_visual.start_graphing(self.lines_data, animate=animate)
