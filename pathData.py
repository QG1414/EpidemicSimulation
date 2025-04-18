from enum import Enum

class PathData:
    def __init__(self, epidemy_treshold):
        self.path_positions = None
        self.state = EpidemyState.STABLE
        self.epidemy_treshold = epidemy_treshold

    def add_path(self, xy):
        self.path_positions = xy
        if xy[1][-1] >= self.epidemy_treshold:
            self.state = EpidemyState.EPIDEMY
        elif xy[1][-1] == 0:
            self.state = EpidemyState.ENDED
        else:
            self.state = EpidemyState.STABLE



class EpidemyState( Enum ):
    STABLE = 0
    EPIDEMY = 1
    ENDED = 2 #TODO change in futute name
