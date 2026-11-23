import scipy
from scipy.optimize import fmin_cg

def f(z):
        x=z[0];y=z[1];
        return (x-1)**2+(y-3)**2


z0 = [0,0]
res=scipy.optimize.fmin_cg(f, z0)

print(res)
