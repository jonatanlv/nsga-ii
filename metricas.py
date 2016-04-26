# -*- coding: utf-8 -*-
"""
En este módulo implementaremos las métricas usadas.
En todos los casos contrastaremos el frente de Pareto con una población
 - pop# siempre se refiere a poblaciones en el espacio de decisiones
 - p# siempre serán puntos en el espacio de soluciones
"""
import numpy as np
import logging

#Medidas de diversidad
def Lambda(pop1, problema):
    '''Descrita en 'A fast and elitist multiobjective genetic algorithm: NSGA-II
    Suponemos que la población está "ordenada" con respecto a los índices'''
    distancias = []
    auxP = None
    for p1 in pop1:
        if auxP is None:
            auxP = p1
            continue
        else:
            distancias.append(distancia(auxP.evaluado_en(problema), p1.evaluado_en(problema)))
            auxP = p1
            
    media = np.mean(distancias)
    
    #DONE esto está mal, no podemos suponer que los extremos de la población son el primero y el último
    #logging.warn('Calculando Lambda. Los extremos puede que no sean los correctos')
    df = minimaDistancia(pop1[0].evaluado_en(problema), [problema.fp['extremos'][0]])
    dl = minimaDistancia(pop1[-1].evaluado_en(problema), [problema.fp['extremos'][1]])
    
    return (df + dl + np.sum(np.abs(distancias - media))) / (df + dl + media * len(distancias))

def Spread(pop1, problema):
    '''Dispersión de la población sin tener en cuenta los puntos extremos'''
    distancias = []
    for p1 in pop1:
        distancias_a_p1 = []
        for p2 in pop1:
            if not p1 is p2:
                distancias_a_p1.append(distancia(p1.evaluado_en(problema), p2.evaluado_en(problema)))
            else:
                distancias_a_p1.append(float('inf'))
        distancias.append(np.min(distancias_a_p1))
    
    return np.std(distancias)

#Medidas de ajuste
def Upsilon(pop1, problema):
    '''Descrita en 'A fast and elitist multiobjective genetic algorithm: NSGA-II'''
    distancias = np.array([minimaDistancia(p.evaluado_en(problema), problema.fp['frente']) for p in pop1])
    return np.mean(distancias)

#Medidas de cobertura
def C(pop1, pop2, problema):
    '''Proporción de soluciones en pop2 que son débilemente domindas por pop1'''
    cont = 0
    for p2 in pop2:
        for p1 in pop1:
            if problema.dominado(p1, p2) > 0:
                cont += 1
                break
    
    return cont / len(pop2)

#Medidas mixtas


#Funciones de apoyo
def minimaDistancia(p1, conjunto, lp = 2):
    '''Devuelve al mínima distancia entre el punto y cada elemento de pop2'''
    minimo = float('inf')
    for p in conjunto:
        psd = distancia(p, p1, lp = 2, raiz = False)
        if psd < minimo:
            minimo = psd
    
    return np.power(minimo, 1 / lp)
        
def distancia(p1, p2, lp = 2, raiz = True):
    suma = np.sum((p1 - p2) ** lp)
    if raiz:
        return float(np.power(suma, 1 / lp))
    else:
        return float(suma)

def extremos(pop1):
    '''Suponemos minimización y lo que buscamos son los extremos'''
    pass