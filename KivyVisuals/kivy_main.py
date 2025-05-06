from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from enums.epidemyEnums import *
from enums.presetEnums import *
from KivyVisuals.kivy_helpers import PositionAdjuster, BaseScreen
from SymulationData import SymulationData


from KivyVisuals.KivySubElements.main.KivyMain import PlagueMainScreen
from KivyVisuals.KivySubElements.loading.KivyLoading import Loading
from KivyVisuals.KivySubElements.settings.KivySettings import CustomSettings
from KivyVisuals.KivySubElements.presets.KivyPresets import SelectPreset

class PlagueApp(App):

    def __init__( self, sd : SymulationData,  **kwargs ):
        pos_adj = PositionAdjuster( Window.size[0], Window.size[1], Window.left, Window.top )
        self.base_screen = BaseScreen( sd, pos_adj )
        super().__init__( **kwargs )

    def build(self):
        return  self.__build_screen_manager()
    
    def __build_screen_manager(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget( PlagueMainScreen( self.base_screen, name = "plague_main_screen" ) )
        screen_manager.add_widget( Loading( self.base_screen, name = "loading" ) )
        screen_manager.add_widget( CustomSettings( self.base_screen, name = "custom_settings" ) )
        screen_manager.add_widget( SelectPreset( self.base_screen, name = "preset_selection" ) )
        return screen_manager

class MainApp:
    def __init__(self, sd : SymulationData ):
        self.__set_basic_params()
        self.pg_app = PlagueApp(sd)
    
    def __set_basic_params(self):
        Config.set('graphics', 'resizable', False)
        Window.size = (600,800)
        Config.write()

    def start_app(self):
        self.pg_app.run() 

