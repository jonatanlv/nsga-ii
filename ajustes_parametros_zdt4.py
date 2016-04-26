# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 18:36:33 2014

@author: jlaraval
"""
from explorador import *
import matplotlib.pyplot as plt

valores = [2, 5, 20, 100]
filtro1 = '100.250.mp.sbx.nstss.none.{}.{}.txt'
lookups = ['Acumulador.Lambda.media', 'Acumulador.Lambda.stddev',
            'Acumulador.Upsilon.media','Acumulador.Upsilon.stddev',
            'Acumulador.no_dominadas.media','Acumulador.no_dominadas.stddev',
            'Acumulador.Spread.media','Acumulador.Spread.stddev']
titulos = [r'$\Lambda$ con respecto a $\eta_c$ y $\eta_m$',
           r'$\Upsilon$ con respecto a $\eta_c$ y $\eta_m$',
           r'Cantidad de soluciones no dominadas con respecto a $\eta_c$ y $\eta_m$',
           r'Spread con respecto a $\eta_c$ y $\eta_m$']
           
ylabels = [r'$\Lambda$', r'$\Upsilon$', r'Soluciones no dominadas', r'Spread']
colores = ['red','blue','cyan','black']

#buscamos los archivos de estadísticas que vamos a emplear
todos = explorador()

archivos = []
for etac in valores:
    for etam in valores:
        archivos.extend(filtro(todos, patron = filtro1.format(etac, etam)))
        
#En archivos ya tenemos todos los archivos que vamos a usar para la gráfica
res = {}
for v in lookups:
    res[v] = {}

for etac in valores:
    for etam in valores:
        #seleccionamos el fichero con etac.etam
        nom = filtro(archivos, patron = filtro1.format(etac, etam))[0]
        #leemos el fichero
        with open(nom) as fin:
            lectura = [l.strip() for l in fin if l.strip() != '']
        #pasamos todos los valores a res
        for v, k in res.items():
            k[(etac, etam)] = lookup(lectura, v)
            
#Ya tenemos en res todos los resultados que necesitamos, el formato es:
#res[parametro] = observaciones
#parametro := valores que hay en lookups
#observaciones := {(2,2): valor.2.2, (2,5): valor.2.5, ... , (100,100): valor.100.100}
#valor.i.j := el valor de la observación que corresponda con etac = i y etam = j

#Queremos dibujar 4 gráficas, cada una de ellas con cuatro errorbar
plt.ioff()
for i in range(0, len(lookups), 2):
#for i in range(0, 1, 2):
    i1 = int(i / 2)
    xs, ys, stds = [], [], []
    xs = valores[:]
    for etam in valores:
        parcial = []
        parcial_err = []
        for etac in valores:
            parcial.append(res[lookups[i]][(etac,etam)])
            parcial_err.append(res[lookups[i + 1]][(etac,etam)])
        ys.append(parcial)
        stds.append(parcial_err)
        
    for j in range(len(ys)):
        plt.errorbar(xs, ys[j], yerr = stds[j], fmt = 'o-', ecolor = colores[j],
                     ms = 8, mec = colores[j], mfc = colores[j], c = colores[j])
        
    plt.xlim(1, 150)
    plt.xscale('log')
    plt.xlabel(r'$\eta_c$')
    plt.xticks(xs, xs)
    plt.title(titulos[i1])
    
    plt.ylabel(ylabels[i1])
    plt.legend([r'$\eta_m = 2$', r'$\eta_m = 5$', r'$\eta_m = 20$', r'$\eta_m = 100$'],
               framealpha = .8)
    
    plt.savefig('memoria\\images\\ajuste_param_zdt4_{}.png'.format(i1), format='png', dpi=300)
    plt.close('all')