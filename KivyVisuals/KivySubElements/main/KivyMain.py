from KivyVisuals.kivy_helpers import BaseScreen, PopupKivy
from kivy.properties import BooleanProperty, StringProperty, NumericProperty

class PlagueMainScreen(BaseScreen):    
    use_animation : BooleanProperty = BooleanProperty(True)
    use_log_scale : BooleanProperty = BooleanProperty(True)
    use_CUDA : BooleanProperty = BooleanProperty(False)

    current_preset : StringProperty = StringProperty("none")

    set_data_width : NumericProperty = NumericProperty(1000)
    set_data_height : NumericProperty = NumericProperty(800)

    def __init__( self, bs : BaseScreen, **kw ) -> None:
        super().__init__( bs.sd, bs.pos_adj, **kw )

        self.current_preset = self.sd.current_preset
        self.set_data_width = 1000
        self.set_data_height = 800
    
#region Toggles

    def change_scale( self, value : bool ) -> None:
        self.use_log_scale, self.sd.use_log = ( value, value )
    
    def change_animate( self, value : bool ) -> None:
        self.use_animation, self.sd.use_animation = ( value, value )

    def change_cuda( self, value : bool ) -> None:
        self.use_CUDA = value
        if( not self.sd.set_cuda( value, True ) ):
            self.use_CUDA = False
            self.show_popup()
    
    def show_popup(self) -> None:
        popKv = PopupKivy("CUDA ERROR", "Cuda wasn't detected on the device so it was autamaticly disabled")
        popKv.show_popup()
    
#endregion Toggles