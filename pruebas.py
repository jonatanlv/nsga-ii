# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 01:37:16 2014

@author: jlaraval
"""

import numpy as np
import matplotlib.pyplot as plt
#from ZDT1 import *
#from ZDT2 import *
from ZDT3 import *
#from ZDT4 import *
#from ZDT5 import *
#from ZDT6 import *

x = np.zeros(30)
puntos = []
for i in np.linspace(0,1,2500):
    x = np.zeros(30)
    x[0] = i
    puntos.append(x)

xs = [f1(p) for p in puntos]
ys = [f2(p) for p in puntos]

'''Con esto sacamos el frente de pareto, sólo válido en dos dimensiones'''
ys.insert(0,float('inf'))
macc = [min(ys[:i]) for y,i in zip(ys, range(1,len(ys)+1))]
fp = [(xx, yy) for xx, yy,m in zip(xs, ys[1:],macc) if yy < m]
xfp = [xx for xx,yy in fp]
yfp = [yy for xx,yy in fp]
plt.plot(xfp, yfp)
plt.plot(xs, ys[1:])