# -*- coding: utf-8 -*-
"""
Función Test con restricciones CONSTR
"""
import Problem
import numpy as np
from Estadisticas import Estadisticas

def construir_problema(**kwargs):
    def f1(X):
        return X[0]
        
    def f2(X):
        return (1 + X[1]) / X[0]
        
    objetivos = [f1, f2]
    
    dimensiones = 2
    
    ''' Los límites de este problema son [0.1, 1]x[0, 5] '''
    limites = np.zeros((dimensiones,2))
    limites[0, 0] = 0.1
    limites[0, 1] = 1
    limites[1, 0] = 0
    limites[1, 1] = 5
    
    ''' Restricciones. Suponemos que todas las restricciones son en la forma f(x) >= 0'''
    def g1(X):
        return X[1] + 9 * X[0] - 6
        
    def g2(X):
        return -X[1] + 9 * X[0] - 1
        
    restricciones = [g1, g2]
    
    ''' Construimos el frente de Pareto asociado a este problema '''
    xs = []
    ys = []
    with open('CONSTR.pf') as fin:
        for l in fin:
            if l.strip() != '':
                xs.append(float(l.strip().split()[0]))
                ys.append(float(l.strip().split()[1]))
    
    fp = {}
    fp['frente'] = np.array(sorted(list(zip(xs, ys)), key = lambda x: x[0]))
    fp['extremos'] = [fp['frente'][0], fp['frente'][-1]]
    
    ''' Parámetros '''
    parametros = Problem.Params()
    parametros.update(kwargs)
    
    ''' Estadísticas '''
    estadisticas = Estadisticas(kwargs.get('nom_stats', 'estadisticas'))
    
    ''' Lo empaquetamos todo '''
    problema = Problem.Problem(objetivos, dimensiones, limites, frentePareto = fp, parametros = parametros, stats = estadisticas, restricciones = restricciones)
    
    return problema