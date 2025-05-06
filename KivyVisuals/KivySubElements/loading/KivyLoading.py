from threading import Thread
from KivyVisuals.kivy_helpers import BaseScreen
from kivy.properties import StringProperty


class Loading(BaseScreen):
    info_text : StringProperty = StringProperty( "Waiting for symulation to load" )

#region init

    def __init__( self, bs : BaseScreen , **kw ):
        super().__init__( bs.sd, bs.pos_adj, **kw )
        self.all_to_load : int = self.sd.spd.k
        self.loaded : int = 0
    
    def update_visuals_on_start(self):
        self.ids.cancle_button.disabled = False
        self.loaded = 0
        self.all_to_load = self.sd.spd.k
        self.info_text = f"symulations: {self.loaded} / {self.all_to_load}"

#endregion init

    def start_symulation(self):
        self.update_visuals_on_start()
        self.sd.restart_data()
        Thread( target = lambda: self.sd.start_load_data(self), daemon=True).start()

    def update_visuals(self, dt):
        self.loaded = dt
        self.info_text = f"symulations: {self.loaded} / {self.all_to_load}"

    def after_loading(self):
        self.ids.cancle_button.disabled = True
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