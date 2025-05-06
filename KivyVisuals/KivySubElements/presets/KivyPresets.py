from KivyVisuals.kivy_helpers import BaseScreen
from kivy.properties import ListProperty, StringProperty
from enums.presetEnums import *

class SelectPreset(BaseScreen):
    presets = ListProperty("none")
    current_name = StringProperty("none")

    def __init__(self, bs : BaseScreen, **kw):
        super().__init__( bs.sd, bs.pos_adj, **kw )
        self.base_presets = {
            PRESETS_NAMES.NONE.value : PRESETS.NONE.value,
            PRESETS_NAMES.COVID.value : PRESETS.COVID.value,
            PRESETS_NAMES.PLAGUE.value : PRESETS.PLAGUE.value,
            PRESETS_NAMES.SPANISH_FLU.value : PRESETS.SPANISH_FLU.value,
            PRESETS_NAMES.VON_ECONOMO_ENCEPHALITIS.value : PRESETS.VON_ECONOMO_ENCEPHALITIS.value
            }
        self.presets = tuple(self.base_presets.keys())

    def on_start_update(self):
        self.current_name = self.sd.current_preset

    def on_preset_save(self):
        if len(self.base_presets.get(self.ids.currentPresetSet.text)) == 0:
            self.sd.current_preset = PRESETS_NAMES.NONE.value
            self.sd.symulation_name = ""
            self.current_name = self.ids.currentPresetSet.text
            return
        self.sd.import_preset_not_static(self.base_presets.get(self.ids.currentPresetSet.text), self.ids.currentPresetSet.text)
        self.current_name = self.ids.currentPresetSet.text