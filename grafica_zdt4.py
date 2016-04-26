# -*- coding: utf-8 -*-
"""
A dibujar
"""
import ZDT4 as test
import matplotlib.pyplot as plt
import numpy as np

archivos = ["Ejecuciones\\ZDT4\\100.250.m1.uc.su.none\\2014.11.04.03.39", \
            "Ejecuciones\\ZDT4\\100.250.mp.sbx.nstss.none\\2014.11.11.05.22",\
            "Ejecuciones\\ZDT4\\100.250.m1.sbx.su.none\\2014.11.09.23.51"]
            
pr = test.construir_problema()

fp = pr.fp['frente']
fpx = [s[0] for s in fp]
fpy = [s[1] for s in fp]

plt.ioff()

x, y = [], []

for i in range(len(archivos)):
    with open(archivos[i] + "\\solucionFinal.txt") as fin:
        lect = [l.strip() for l in fin]
    
    lect = [l.replace("[", "") for l in lect]
    lect = [l.replace("]", "") for l in lect]
    lect = [l.strip() for l in lect]
    
    x.append([float(l.split()[0]) for l in lect])
    y.append([float(l.split()[1]) for l in lect])

estilo = ['g*','bd','rH']

ps = []
for i in range(len(archivos)):
    ps.append(plt.plot(x[i], y[i], estilo[i]))
    
ps.append(plt.plot(fpx, fpy, 'k.-'))
plt.ylim(0,8.5)
plt.title('Mejores soluciones encontradas para ZDT4')
plt.xlabel('$f_1$')
plt.ylabel('$f_2$')
plt.legend(('m1.uc.su','mp.sbx.nstss','m1.sbx.su','Frente Pareto'))
plt.show()
