from threading import Thread
from KivyVisuals.kivy_helpers import BaseScreen
from kivy.properties import StringProperty


class Loading(BaseScreen):
    info_text : StringProperty = StringProperty( "0%" )

#region init

    def __init__( self, bs : BaseScreen , **kw ):
        super().__init__( bs.sd, bs.pos_adj, **kw )
        self.all_quick_load : int = self.sd.spd.k * self.sd.spd.n
    
    def update_visuals_on_start(self):
        self.ids.symulations_number.font_size = 100
        self.ids.cancle_button.disabled = False
        self.all_quick_load : int = self.sd.spd.k * self.sd.spd.n
        self.info_text = f"{round( (0 / self.all_quick_load) *100 )}%"

#endregion init

    def start_symulation(self):
        self.update_visuals_on_start()
        self.sd.restart_data()
        Thread( target = lambda: self.sd.start_load_data(self), daemon=True).start()
    
    def quick_update(self, dt):
        self.ids.symulations_number.filled = 360 * ( dt / self.all_quick_load )
        self.info_text = f"{round( (dt / self.all_quick_load) * 100 )}%"

    def after_loading(self):
        self.ids.cancle_button.disabled = True
        self.ids.symulations_number.font_size = 50
        self.info_text = "Close graph to return to mainScreen"

    def finish_loading(self):
        self.sd.start_graphing(self.sd.use_animation)
        self.back_to_main()
    
#region return to main

    def cancel_loading(self):
        self.sd.force_cancel()

    def back_to_main(self):
        self.manager.transition.direction = "right"
        self.manager.transition.duration = 0.2
        self.manager.current = "plague_main_screen"

#endregion return to main