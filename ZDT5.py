# -*- coding: utf-8 -*-
"""
Función Test ZDT5
"""

import Problem
import numpy as np
from Estadisticas import Estadisticas

def construir_problema(**kwargs):
    def f1(X):
        x0 = X.fenotipo()[0]
        return 1 + x0.sum()
        
    def u(X):
        return np.sum(X)
        
    def v(x):
        if x < 5:
            return 2 + x
        else:
            return 1
        
    def f2(X):
        f1x = f1(X)
        fenotipo = X.fenotipo()
        suma = 0
        for i in range(1, len(fenotipo)):
            suma += v(u(fenotipo[i]))
        return  1 / f1x * suma
        
    objetivos = [f1, f2]
    
    dimensiones = 30 + 5 * 10 #Cantidad de unos y ceros
    
    ''' Los límites de este problema son [0,1]^30 '''
    limites = np.zeros((dimensiones,2))
    limites[:, 0] = 0
    limites[:, 1] = 1
    
    ''' Construimos el frente de Pareto asociado a este problema '''
    xs = list(range(1, 32))
    ys = [10 / x for x in xs]
    
    fp = {}
    fp['frente'] = np.array(list(zip(xs, ys)))
    fp['extremos'] = [fp['frente'][0], fp['frente'][-1]]
    
    ''' Parámetros '''
    parametros = Problem.Params()
    parametros.update(kwargs)
    parametros['dist_fenotipo'] = [30, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    parametros['tipo_var'] = 'bin'
    
    ''' Extras '''
    extras = Problem.Params()
    extras.update({'dtype': 'bool'})    
    
    ''' Estadísticas '''
    estadisticas = Estadisticas(kwargs.get('nom_stats', 'estadisticas'))
    
    ''' Lo empaquetamos todo '''
    problema = Problem.Problem(objetivos, dimensiones, limites, frentePareto = fp, parametros = parametros, stats = estadisticas, extras = extras)
    
    return problema