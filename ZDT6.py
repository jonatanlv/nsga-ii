# -*- coding: utf-8 -*-
"""
Función Test ZDT6
"""
import Problem
import numpy as np
from Estadisticas import Estadisticas

def construir_problema(**kwargs):
    
    def f1(X):
        return 1 - np.exp(-4*X[0]) * np.sin(6*np.pi*X[0]) ** 6
        
    def g(X):
        return 1 + 9 * (X[1:].sum() / (len(X) - 1)) ** .25
        
    def f2(X):
        gX = g(X)
        return gX * (1 - (f1(X) / gX)**2)
        
    objetivos = [f1, f2]
    
    dimensiones = 10
    
    ''' Los límites de este problema son [0,1]^10 '''
    limites = np.zeros((dimensiones, 2))
    limites[:, 0] = 0
    limites[:, 1] = 1
    
    ''' Construimos el frente de Pareto asociado a este problema x2 = 1 - x1^2'''
    '''http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/zdt6/index.php'''
    xs = np.linspace(.2807753191, 1, 500)
    ys = 1 - (xs)**2
    
    fp = {}
    fp['frente'] = np.array([(xx, yy) for xx, yy in zip(xs, ys)])
    fp['extremos'] = [fp['frente'][0], fp['frente'][-1]]
    
    ''' Parámetros '''
    parametros = Problem.Params()
    parametros.update(kwargs)
    
    ''' Estadísticas '''
    estadisticas = Estadisticas(kwargs.get('nom_stats', 'estadisticas'))
    
    ''' Lo empaquetamos todo '''
    problema = Problem.Problem(objetivos, dimensiones, limites, frentePareto = fp, parametros = parametros, stats = estadisticas)
    
    return problema
