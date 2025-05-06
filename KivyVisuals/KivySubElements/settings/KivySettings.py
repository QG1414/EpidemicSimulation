from SymulationData import SymulationPreData
from KivyVisuals.kivy_helpers import BaseScreen
from kivy.properties import ListProperty, BooleanProperty
from enums.epidemyEnums import *
from generationScripts.generation import GenerationData

class CustomSettings(BaseScreen):
    modifiersValuesVisual = ListProperty()
    vaccines = BooleanProperty(False)

    #region init

    def __init__(self, bs : BaseScreen, **kw):     
        super().__init__( bs.sd, bs.pos_adj, **kw ) 

        self.modifiersDict = {
            MODIF_LEVELS.VERY_BAD.name : MODIF_LEVELS.VERY_BAD,
            MODIF_LEVELS.BAD.name : MODIF_LEVELS.BAD,
            MODIF_LEVELS.NORMAL.name : MODIF_LEVELS.NORMAL,
            MODIF_LEVELS.GOOD.name : MODIF_LEVELS.GOOD,
            MODIF_LEVELS.VERY_GOOD.name : MODIF_LEVELS.VERY_GOOD
        }

        self.modifiersValuesVisual = tuple( self.modifiersDict.keys() )

        self.generation_params = {
            self.ids.generationSize : int, 
            self.ids.curingTimeMin : int , 
            self.ids.curingTimeMax : int, 
            self.ids.curingChance : float, 
            self.ids.resistanceTimeMin : int, 
            self.ids.resistanceTimeMax : int
        }

        self.rest_of_params = {
            self.ids.ChanceToMeet : str,
            self.ids.daysToSimulate : int,
            self.ids.simulationsToRun : int,
            self.ids.chanceToInfect : float 
        }

        self.modif_params = [self.ids.hygieneModif, self.ids.popModif, self.ids.healthModif]
        self.vaccines_params = {self.ids.populationVaccinated : float, self.ids.dayOfVaccinesCreation : int}
    
    #endregion init

    #region OnStartSetup 

    def setup_data(self):
        current_data, modif = self.sd.get_current_data()
        self.setup_base_params( current_data )
        self.setup_modif_params( modif )
    
    def setup_base_params(self, data : list[any] ) -> None:
        for index, ui in enumerate(list(self.generation_params.keys()) + list(self.rest_of_params.keys()) ):
            if not isinstance(data[index], dict):
                ui.text = str(round(data[index],2))
            else:
                final_str = ""
                for key,value in data[index].items():
                    final_str += str(key) + " " + str(round(value, 2)) + "\n"
                final_str = final_str[:-1]
                ui.text = final_str

    def setup_modif_params( self, data : dict[ str, any ]):
        for index, ui in enumerate(self.modif_params):
            ui.text = list(data.values())[index].name
        
        self.vaccines = list(data.values())[-2].value

        for index, value in enumerate( list(data.values())[-1].values() ):
            list(self.vaccines_params.keys())[index].text = str(value)

    #endregion OnStartSetup 

    def save_changes(self):
        self.sd.update_all_data( self.create_generation(), self.create_symulation_data(), self.generate_modifs(), self.vaccines, self.generate_vaccines() )

    #region ChangesGeneration

    def create_generation(self) -> GenerationData:
        generation_params = []
        for key, value in self.generation_params.items():
            generation_params.append(value(key.text))
        generation_params.insert(1, self.sd.gd.epidemy_treshold)
        return GenerationData(*generation_params)
    
    def create_symulation_data(self) -> SymulationPreData:
        rest_of_params = []
        for key, value in self.rest_of_params.items():
            if value == str:
                rest_of_params.append( self.generate_chance_to_meet(key) )
            else:
                rest_of_params.append( value(key.text) )

        return SymulationPreData(*rest_of_params)

    def generate_chance_to_meet( self, key ):
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
            vaccines_params.append( value(key.text) )
        return vaccines_params
    
    #endregion ChangesGeneration