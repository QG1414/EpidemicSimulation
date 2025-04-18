from pathsGenerator import PathsGeneratorCalculus, PathsGeneratorVisual

n = 20  # steps per path
m = 2   # number of people infected after meeting
p = 0.9
k = 15   # number of paths
curing_time = 2
threshold = 30

pgc = PathsGeneratorCalculus(threshold)


lines_data = pgc.generate_paths(n, m, p, k)

y_min = float("inf")
y_max = threshold + 5
for i in lines_data:
    y_min = min( y_min, min( i.path_positions[1] ) )
    y_max = max( y_max, max( i.path_positions[1] ) )

pgv = PathsGeneratorVisual(n,k,threshold)
pgv.set_y_scale(y_min, y_max)
pgv.start_animation(lines_data)