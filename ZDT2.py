# -*- coding: utf-8 -*-
"""
Función Test ZDT2
"""
import numpy as np
import Problem
from Estadisticas import Estadisticas

def construir_problema(**kwargs):
    
    def f1(X):
        return X[0]
        
    def g(X):
        return 1 + 9*X[1:].sum()/(len(X) - 1)
        
    def f2(X):
        gX = g(X)
        return gX * (1 - np.power(f1(X) / gX, 2))
    
    objetivos = [f1, f2]
    
    dimensiones = 30
    
    ''' Los límites de este problema son [0,1]^30 '''
    limites = np.zeros((dimensiones,2))
    limites[:, 0] = 0
    limites[:, 1] = 1
    
    ''' Construimos el frente de Pareto asociado a este problema '''
    soluciones = []
    for i in np.linspace(0, 1, 500):
        solucion = np.zeros(dimensiones)
        solucion[0] = i
        soluciones.append(solucion)
    
    xs = [f1(p) for p in soluciones]
    ys = [f2(p) for p in soluciones]
    
    ys.insert(0,float('inf'))
    macc = [min(ys[:i]) for y, i in zip(ys, range(1,len(ys)+1))]
    fp = {}
    fp['frente'] = np.array([(xx, yy) for xx, yy,m in zip(xs, ys[1:],macc) if yy < m])
    fp['extremos'] = [fp['frente'][0], fp['frente'][-1]]
    
    ''' Parámetros '''
    parametros = Problem.Params()
    parametros.update(kwargs)
    
    ''' Estadísticas '''
    estadisticas = Estadisticas(kwargs.get('nom_stats', 'estadisticas'))
    
    ''' Lo empaquetamos todo '''
    problema = Problem.Problem(objetivos, dimensiones, limites, frentePareto = fp, parametros = parametros, stats = estadisticas)
    
    return problema