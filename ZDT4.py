# -*- coding: utf-8 -*-
"""
Función Test ZDT4
"""
import Problem
import numpy as np
from Estadisticas import Estadisticas

def construir_problema(**kwargs):
    
    def f1(X):
        return X[0]
        
    def g(X):
        return 1 + 10 * (len(X) - 1) + (X[1:]**2).sum() - 10 * (np.cos(4 * np.pi * X[1:])).sum()
        
    def f2(X):
        gX = g(X)
        return gX * (1 - np.sqrt(f1(X) / gX))
        
    objetivos = [f1, f2]
    
    dimensiones = 10
    
    ''' Los límites de este problema son [0,1] x [-5,5]^29 '''
    limites = np.zeros((dimensiones, 2))
    limites[:, 0] = -5
    limites[:, 1] = 5
    limites[0, 0] = 0
    limites[0, 1] = 1
    
    ''' Construimos el frente de Pareto asociado a este problema x2 = 1 - sqrt(x1)'''
    '''http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/zdt4/index.php'''
    xs = np.linspace(0, 1, 500)
    ys = 1 - np.sqrt(xs)
    
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
