from kivy.uix.screenmanager import Screen
from SymulationData import SymulationData
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

class PositionAdjuster:
    def __init__( self, base_width : int, base_height : int, base_width_pos : int, base_height_pos : int ):
        self.__base_width : int = base_width
        self.__base_height : int = base_height
        self.__base_width_pos : int = base_width_pos
        self.__base_height_pos : int = base_height_pos

    def get_base_size(self) -> tuple[int, int]:
        return ( self.__base_width, self.__base_height )
    
    def get_base_pos(self) -> tuple[int, int]:
        return ( self.__base_width_pos, self.__base_height_pos )

    def calculate_new_position(self, new_width : int , new_height : int ) -> tuple[int, int]:
        return ( self.__calculate_new_width_pos( new_width ), self.__calculate_new_height_pos( new_height ) )

    def __calculate_new_width_pos( self, new_width : int ) -> int:
        return ( self.__base_width_pos + ( self.__base_width - new_width ) / 2 )

    def __calculate_new_height_pos( self, new_height : int ) -> int:
        return ( self.__base_height_pos + ( self.__base_height - new_height ) / 2 )

class BaseScreen(Screen):
    def __init__( self, sd : SymulationData, pos_adj : PositionAdjuster, **kw ):
        self.sd : SymulationData = sd
        self.pos_adj : PositionAdjuster = pos_adj
        super().__init__(**kw)
    
    def resize_window( self, new_width : int, new_height : int ):
        Window.size = ( new_width, new_height )
        Window.left, Window.top = self.pos_adj.calculate_new_position( new_width, new_height )

class PopupKivy(FloatLayout):

    label_text = StringProperty("")

    def __init__(self, title : str, label_text : str, **kwargs):
        self.label_text = label_text
        self.title = title
        super().__init__(**kwargs)

    def show_popup(self):
        self.pop_window = Popup(title=self.title, content = self, size_hint = (None, None), size = (400,400), separator_color = [0,0,0,0])
        self.pop_window.open()
    
    def close_popup(self):
        if self.pop_window != None:
            self.pop_window.dismiss()
        self.pop_window = None