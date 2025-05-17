from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '800')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from enums.epidemyEnums import *
from enums.presetEnums import *
from KivyVisuals.kivy_helpers import PositionAdjuster, BaseScreen
from SymulationData import SymulationData
from kivy.core.window import Window

from KivyVisuals.KivySubElements.templates.CustomSpinner import CustomSpinner
from KivyVisuals.KivySubElements.main.KivyMain import PlagueMainScreen
from KivyVisuals.KivySubElements.loading.KivyLoading import Loading
from KivyVisuals.KivySubElements.settings.KivySettings import CustomSettings
from KivyVisuals.KivySubElements.presets.KivyPresets import SelectPreset
from helper import resource_path

class PlagueApp(App):

    icon = resource_path('KivyVisuals\images\Icon.png')

    @staticmethod
    def resource_path_app(relative_path):
        return resource_path(relative_path)

    def __init__( self, sd : SymulationData,  **kwargs ) -> None:
        self.sd = sd
        super().__init__( **kwargs )

    def build( self ) -> any:
        return  self.__build_screen_manager()
    
    def __build_screen_manager( self ) -> ScreenManager:
        pos_adj = PositionAdjuster( Window.width, Window.height, Window.left, Window.top )
        base_screen = BaseScreen( self.sd, pos_adj )

        screen_manager = ScreenManager()
        screen_manager.add_widget( PlagueMainScreen( base_screen, name = "plague_main_screen" ) )
        screen_manager.add_widget( Loading( base_screen, name = "loading" ) )
        screen_manager.add_widget( CustomSettings( base_screen, name = "custom_settings" ) )
        screen_manager.add_widget( SelectPreset( base_screen, name = "preset_selection" ) )
        return screen_manager

class MainApp:
    def __init__( self, sd : SymulationData ) -> None:
        self.pg_app = PlagueApp(sd)
    
    def start_app( self ) -> None:
        self.pg_app.run() 

