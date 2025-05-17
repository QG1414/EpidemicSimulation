from SymulationData import SymulationPreData
from KivyVisuals.kivy_helpers import BaseScreen, PopupKivy
from kivy.properties import ListProperty, BooleanProperty
from enums.epidemyEnums import *
from generationScripts.generation import GenerationData
from kivy.clock import Clock
import numpy as np

class CustomSettings(BaseScreen):
    modifiersValuesVisual = ListProperty()
    vaccines = BooleanProperty(False)

    #region init

    def __init__( self, bs : BaseScreen, **kw ) -> None:     
        super().__init__( bs.sd, bs.pos_adj, **kw ) 

        self.modifiersDict : dict[str, MODIF_LEVELS] = {
            MODIF_LEVELS.VERY_BAD.name : MODIF_LEVELS.VERY_BAD,
            MODIF_LEVELS.BAD.name : MODIF_LEVELS.BAD,
            MODIF_LEVELS.NORMAL.name : MODIF_LEVELS.NORMAL,
            MODIF_LEVELS.GOOD.name : MODIF_LEVELS.GOOD,
            MODIF_LEVELS.VERY_GOOD.name : MODIF_LEVELS.VERY_GOOD
        }

        self.modifiersValuesVisual : tuple[MODIF_LEVELS] = tuple( self.modifiersDict.keys() )

    
    def setup_ids( self, *args ) -> None:
        self.generation_params : dict[any, tuple[type, any]] = {
            self.ids.generationSize : (int, self.sd.gd.generation_size), 
            self.ids.curingTimeMin : (int, self.sd.gd.curing_time_min) , 
            self.ids.curingTimeMax : (int, self.sd.gd.curing_time_max), 
            self.ids.curingChance : (float, self.sd.gd.base_curing_prob), 
            self.ids.resistanceTimeMin : (int, self.sd.gd.resTime_min), 
            self.ids.resistanceTimeMax : (int, self.sd.gd.resTime_max)
        }

        self.rest_of_params : dict[any, tuple[type, any]] = {
            self.ids.ChanceToMeet : (str, self.sd.spd.base_chance_to_meet),
            self.ids.daysToSimulate : (int, self.sd.spd.n),
            self.ids.simulationsToRun : (int, self.sd.spd.k),
            self.ids.chanceToInfect : (float, self.sd.spd.p) 
        }

        self.modif_params : list[any] = [self.ids.hygieneModif, self.ids.popModif, self.ids.healthModif]

        self.vaccines_params : dict[any, tuple[type, any]] = {
            self.ids.populationVaccinated : (float, self.sd.get_vaccines_params(VACCINES_PARAMS.POPULATION_VACCINATED)), 
            self.ids.dayOfVaccinesCreation : (int, self.sd.get_vaccines_params(VACCINES_PARAMS.DAY_OF_VACCINES))
        }
    
    #endregion init

    #region OnStartSetup 

    def setup_data( self ) -> None:
        self.setup_ids()
        current_data, modif = self.sd.get_current_data()
        self.setup_base_params( current_data )
        self.setup_modif_params( modif )
    
    def setup_base_params( self, data : list[any] ) -> None:
        for index, ui in enumerate(list(self.generation_params.keys()) + list(self.rest_of_params.keys()) ):
            if not isinstance(data[index], dict):
                ui.text = str(round(data[index],2))
            else:
                ui.text = self.generate_str_meet(data[index])

    def setup_modif_params( self, data : dict[ str, any ] ) -> None:
        for index, ui in enumerate(self.modif_params):
            ui.text = list(data.values())[index].name
        
        self.vaccines = list(data.values())[-2].value

        for index, value in enumerate( list(data.values())[-1].values() ):
            list(self.vaccines_params.keys())[index].text = str(value)


    #endregion OnStartSetup 

    def save_changes( self ) -> None:
        self.sd.update_all_data( self.create_generation(), self.create_symulation_data(), self.generate_modifs(), self.vaccines, self.generate_vaccines())
        

    #region ChangesGeneration

    def create_generation( self ) -> GenerationData:
        generation_params = []
        for key, value in self.generation_params.items():
            if len(key.text) == 0:
                generation_params.append(value[1])
                continue

            generation_params.append(value[0](key.text))
        generation_params.insert(1, self.sd.gd.epidemy_treshold)
        return GenerationData(*generation_params)
    
    def create_symulation_data( self ) -> SymulationPreData:
        rest_of_params = []
        for key, value in self.rest_of_params.items():
            if value[0] == str:
                if len(key.text) == 0:
                    rest_of_params.append( value[1] )
                    continue

                rest_of_params.append( self.generate_num_meet(key) )
            else:
                if len(key.text) == 0:
                    rest_of_params.append( value[1] )
                    continue
                rest_of_params.append( value[0](key.text) )

        return SymulationPreData(*rest_of_params)


    def generate_str_meet( self, data : dict ) -> str:
        final_str = ""
        for key,value in data.items():
            final_str += str(key) + " " + str(round(value, 2)) + "\n"
        final_str = final_str[:-1]
        return final_str

    def generate_num_meet( self, key : any ) -> dict[int, float]:
        lines = key.text.split("\n")
        chance_to_meet_dict = {}
        for i in lines:
            elements = i.split(" ")
            chance_to_meet_dict.setdefault( int(elements[0]), float(elements[1]) )
        return chance_to_meet_dict

    def generate_modifs( self ) -> list[MODIF_LEVELS]:
        modifs = []
        for i in self.modif_params:
            modifs.append( self.modifiersDict.get( i.text, MODIF_LEVELS.NORMAL ) )
        return modifs
    
    def generate_vaccines( self ) -> list[any]:
        vaccines_params = []
        for key, value in self.vaccines_params.items():
            if len(key.text) == 0:
                vaccines_params.append( value[1] )
                continue

            vaccines_params.append( value[0](key.text) )
        return vaccines_params
    
    #endregion ChangesGeneration



    def checkCorrectValuesInt( self, input_field : any, too_big : int, negative : bool = False, show_to_big_warning = True ) -> None: 
        if input_field.focused:
            return

        if len(input_field.text) == 0:
            return

        if int(input_field.text) < 0 and not negative:
            input_field.text = str(too_big)
            pop = PopupKivy( "ERROR Incorrect Value", "Field shouldn't be negative!" )
            pop.show_popup()
        
        if int(input_field.text) > too_big and show_to_big_warning:
            pop = PopupKivy( "WARNING Big Value", f"Value is big, might cause long loading, try using CUDA\nrecomended max value = {too_big}" )
            pop.show_popup()
    
    def checkCorrectValuesFloat( self, input_field : any, too_big : float, negative : bool = False ) -> None: 
        if input_field.focused:
            return
        
        if len(input_field.text) == 0:
            return
        
        if float(input_field.text) > too_big or (float(input_field.text) < 0 and not negative):
            input_field.text = str(too_big)
            pop = PopupKivy( "ERROR Incorrect Value", "Probability should be between 0 an 1!" )
            pop.show_popup()
        
    def checkChanceToMeet( self, input_field : any ) -> None:     
        if input_field.focused:
            return

        if len(input_field.text) == 0:
            return

        lines = input_field.text.split("\n")
        chance_to_meet_dict = {}
        for i in lines:
            elements = i.split(" ")

            if len(elements) != 2:
                self.revertChanceToMeet(input_field, "ERROR Incorrect Format", "<Chance to meet> found unexpected format be sure to write elements like this:\n\n0 0.2\n1 0.8")
                return
            
            if not elements[0].isdigit():
                self.revertChanceToMeet(input_field, "ERROR Incorrect Value", "<Chance to meet> number of people is not a correct number select number from [0,inf]")
                return
            
            num = int(elements[0])
            ctm = 0

            try:
                ctm = float(elements[1])

                if ctm < 0 or ctm > 1:
                    raise Exception()
            except:
                self.revertChanceToMeet(input_field, "ERROR Incorrect Value", "<Chance to meet> probability is not a correct number select number from [0,1]")
                return
            
            if num in chance_to_meet_dict.keys():
                self.revertChanceToMeet(input_field, "ERROR Incorrect Value", "<Chance to meet> number of people cannot have two identical values")
                return
            
            chance_to_meet_dict.setdefault( num, ctm )
        
        if not np.isclose( sum( chance_to_meet_dict.values() ), 1):
            self.revertChanceToMeet(input_field, "ERROR Incorrect Probability", "<Chance to meet> all probability should add up to 1 no more no less")
            return

    def revertChanceToMeet( self, input_field : any, title : str, message : str ) -> None:
        pop = PopupKivy( title, message )
        pop.show_popup()
        input_field.text = self.generate_str_meet(self.rest_of_params.get(self.ids.ChanceToMeet)[1])
