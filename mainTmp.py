import numpy as np
import pylab

def random_sum(m, p, N):
    if N == 0:
        return 0
    Z = 0
    for j in range(N):
        Z += m*np.random.binomial(1, p)
    return Z

print(random_sum(2, 0.71, 3))

def random_path(n,m,p):
    x = [0]
    y = [1]

    tmp_Z = 1

    for i in range(1, n+1):
        Z = random_sum(m, p, tmp_Z)
        tmp_Z = Z
        x.append(i)
        y.append(Z)
    return x, y

def generate_paths(n,m,p,k):
    for i in range(k):
        x,y = random_path(n,m,p)
        pylab.plot(x,y)
    pylab.grid(True)
    return pylab.show()

n = 20
m = 2
p = 0.6
k = 20

generate_paths(n,m,p,k)