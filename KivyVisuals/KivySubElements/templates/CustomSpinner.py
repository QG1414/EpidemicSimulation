from kivy.uix.spinner import Spinner
from kivy.properties import NumericProperty


class CustomSpinner(Spinner):
    end_pos_x = NumericProperty(0)
    end_pos_y = NumericProperty(0)
    pos_diff = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos = self.update_end_pos, size = self.update_end_pos)
    
    def update_end_pos(self, *args):
        self.end_pos_x = self.pos[0] + self.width
        self.end_pos_y = self.pos[1]
        self.pos_diff = (self.height / 2)