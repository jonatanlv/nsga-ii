# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 00:59:22 2014

@author: jlaraval
"""

import matplotlib.pyplot as plt
import numpy as np

x1 = [1,1.9,3]
y1 = [3, 1.8, 1]
x2 = [2,3]
y2 = [3.5,2]
x3 = [3]
y3 = [3]

plt.subplot(2,2,1)
l1, l2, l3 = plt.plot(x1, y1, 'ko', x2, y2, 'ko', x3, y3, 'ko')
plt.title('Paso 0')
plt.xlim(0,6)
plt.ylim(0,5)
plt.tick_params(axis='both',which='both',\
    bottom='off', top='off', left='off', right='off',\
    labelbottom='off', labeltop='off', labelleft='off', labelright='off')
plt.legend((l3,), ('$\mathcal{P}$',))

plt.subplot(2,2,2)
plt.title('Paso 1')
l1, l2, l3 = plt.plot(x1, y1, 'r*', x2, y2, 'ko', x3, y3, 'ko')
plt.xlim(0,6)
plt.ylim(0,5)
plt.tick_params(axis='both',which='both',\
    bottom='off', top='off', left='off', right='off',\
    labelbottom='off', labeltop='off', labelleft='off', labelright='off')
plt.legend((l1,), ('$\mathcal{F}_1$', ))

plt.subplot(2,2,3)
plt.title('Paso 2')
l1, l2, l3 = plt.plot(x1, y1, 'r*', x2, y2, 'b*', x3, y3, 'ko')
plt.xlim(0,6)
plt.ylim(0,5)
plt.tick_params(axis='both',which='both',\
    bottom='off', top='off', left='off', right='off',\
    labelbottom='off', labeltop='off', labelleft='off', labelright='off')
plt.legend((l1,l2), ('$\mathcal{F}_1$', '$\mathcal{F}_2$'))

plt.subplot(2,2,4)
plt.title('Paso 3')
l1, l2, l3 = plt.plot(x1, y1, 'r*', x2, y2, 'b*', x3, y3, 'g*')
plt.xlim(0,6)
plt.ylim(0,5)
plt.tick_params(axis='both',which='both',\
    bottom='off', top='off', left='off', right='off',\
    labelbottom='off', labeltop='off', labelleft='off', labelright='off')
plt.legend((l1,l2,l3), ('$\mathcal{F}_1$', '$\mathcal{F}_2$', '$\mathcal{F}_3$'))

plt.show()