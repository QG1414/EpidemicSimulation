import numpy as np
from pathData import PathData
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.axes import Axes


class PathsGeneratorCalculus:

    def __init__( self, threshold:int ) -> None:
        self.threshold:int = threshold

    def __random_sum( self, m:int, p:int, N:int ) -> int:
        if N == 0:
            return 0
        Z = 0
        for j in range(N):
            Z += m*np.random.binomial(1, p)
        return Z

    def __random_path( self, n:int ,m:int ,p:int ) -> tuple[int, int]:
        x = [0]
        y = [1]

        tmp_Z = 1

        for i in range(1, n+1):
            Z = self.__random_sum(m, p, tmp_Z)
            tmp_Z = Z
            x.append(i)
            y.append(Z)
        return x, y

    def generate_paths( self, n:int ,m:int ,p:int ,k:int ) -> list[PathData]:
        lines_data = []

        for i in range(k):
            lines_data.append(PathData(self.threshold))
            lines_data[i].add_path(self.__random_path(n,m,p))
        return lines_data
    

    
class PathsGeneratorVisual:

    def __init__( self, n:int, k:int, threshold:int ) -> None:
        self.n : int = n
        self.k : int = k
        self.threshold : int = threshold
        self.fig : Figure
        self.ax : Axes
        self.fig , self.ax = plt.subplots()
        self.__base_visuals()
        self.__update_text([0,0,0])
    
    def __base_visuals( self ) -> None:
        self.lines : list[list[Line2D]] = []
        for _ in range(self.k):
            line, = self.ax.plot([], [], lw=2)
            self.lines.append(line)

        self.treshold_line : list[Line2D] = self.ax.plot(
            [x for x in range(self.n+1)],
            [self.threshold]*(self.n+1),
            linewidth=3
        )
        self.ax.set_xlim(0, self.n)

    
    def set_y_scale( self, min : int , max : int, linthresh=0.5 ) -> None:
        self.ax.set_ylim(min,max)
        self.ax.set_yscale('symlog', linthresh=linthresh)

    def __update_text_with_condition( self, lines_data : list[PathData], end_index:int ) -> None:
        states = [ 0, 0, 0 ]
        for i in lines_data[:end_index]:
            states[i.state.value] += 1
        self.__update_text(states)
    
    def __update_text( self, states:list[int] ) -> None:
        self.fig.texts.clear()
        self.fig.text(.75,.83,f"Stable: {states[0]}")
        self.fig.text(.75,.78,f"Epidemy: {states[1]}")
        self.fig.text(.75,.73,f"Ended: {states[2]}")


    def __init(self) -> list[list[Line2D]]:
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def __update( self, frame : int, lines_data : PathData ) -> list[list[Line2D]]:
        path_index = frame // self.n
        step = ( frame % self.n ) + 1


        for i, line in enumerate(self.lines):
            if i < path_index:
                x, y = lines_data[i].path_positions
                line.set_data(x, y)
            elif i == path_index:
                x, y = lines_data[i].path_positions
                line.set_data(x[:step], y[:step])

                self.__update_text_with_condition( lines_data, i )
            else:
                line.set_data([], [])

        if( frame == (self.n * self.k) ):
            self.__update_text_with_condition( lines_data, len(lines_data) + 1 )
        return self.lines

    def start_animation( self, lines_data ) -> FuncAnimation:
        ani = FuncAnimation(
            self.fig,
            lambda frame : self.__update(frame, lines_data),
            frames=(self.n * self.k)+1,
            init_func= lambda : self.__init(),
            blit=False,
            interval=50,
            repeat=False
        )

        plt.show()
        return ani