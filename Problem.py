# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 20:06:20 2014

@author: jlaraval
"""
import numpy as np
from Estadisticas import Estadisticas

class ProblemException(Exception): pass

class Problem(object):
    '''Define un problema en general, las clases que hereden de este tienen que
    proveer implementaciones'''
    def __init__(self, objetivos, dims, lims, restricciones = None,\
    frentePareto = None, parametros = None, operadores = None, stats = None, extras = None):
        '''Inicializador del problema:
        objetivos: iterable de funciones (se supone minimización)
        dims: dimensiones del espacio de soluciones
        lims: hipercubo con los límites en cada dimensión (iterable de 2-tuples)
        restricciones: conjunto de funciones booleanas para comprobar si una
            solución es válida. None por defecto.
        frentePareto: diccionario con dos claves:
            frente: el frente completo, un iterable con las imágenes de las soluciones
            extremos: las imágenes extremas, para algunas métricas
        parametros: Parametros de todo el proceso
        operadores: operadores evolutivos usados en el problema
        stats: módulo de estadisticas
        '''
        self.objetivos = objetivos
        #Comprobamos la coherencia de n y lims
        if dims != len(lims):
            raise ProblemException('n no coincide con la dimensión de lims')
        else:
            for i in range(dims):
                if len(lims[i]) != 2:
                    raise ProblemException('El elemento ' + str(i) + ' de lims no tiene dos componentes')
                elif lims[i][0] >= lims[i][1]:
                    raise ProblemException('Límites incongruentes lims[{}] = [{}, {}]'.format(i, lims[i][0], lims[i][1]))
        self.dims = dims
        self.lims = lims
        if restricciones == None:
            self.restricciones = []
        else:
            self.restricciones = restricciones
        
        self.evops = operadores        
        
        self.parametros = parametros

        if stats is None:
            self.stats = Estadisticas(self.parametros.get('nom_stats', 'estadisticas'))
        else:
            self.stats = stats
        self.stats.nuevo_Contador('evals') # Número de evaluaciones de los objetivos
        
        self.fp = frentePareto
        
        if extras is None:
            self.extras = Params()
        else:
            self.extras = extras
    
    def __call__(self, *args):
        '''Hacemos que el problema sea una función'''
        return self.evaluador(*args)
    
    def evaluador(self, *args):
        '''Evalúa todos los bojetivos en un punto'''
        self.stats['evals']()
        return np.array([o(*args) for o in self.objetivos])
        
    def en_el_dominio(self, x):
        '''comprobamos que x está dentro de los límites'''
        return np.all(np.logical_and(self.lims[:,0] <= x, x <= self.lims[:,1]))
        
    def violacion_restricciones(self, x):
        '''comprobamos el nivel de violación de las restricciones'''
        suma = 0
        for f in self.restricciones:
            if f(x) < 0:
                suma += -f(x)
        return suma

    def dominado(self, x, y):
        '''x, y son puntos del espacio de búsqueda.
        Devuelve:
        1 si x domina a y
        0 si x no domina a y ni y a x
        -1 si y domina a x
        '''
        ox = x.evaluado_en(self)
        oy = y.evaluado_en(self)
        
        dom1 = ox < oy #Si es todo verdad x domina a y
        dom0 = ox == oy 
        dom_1 = ox > oy #Si es todo verdad y domina a x
        
        if len(ox) == np.sum(dom1) + np.sum(dom0) and np.sum(dom1) > 0:
            return 1
        elif len(oy) == np.sum(dom_1) + np.sum(dom0) and np.sum(dom_1) > 0:
            return -1
        else:
            return 0
    
    def dominadoC(self, x, y):
        '''Dominancia con restricciones
        Devuelve:
        1 si x es factible e y no
        -1 si x no es factible pero y si
        dominado(x,y) si x e y son factibles
        1 si ambos son infactibles pero la violacion de x es menor que la de y
        -1 si ambos son infactibles pero la violacion de y es menor que la de x
        0 en caso contrario
        '''
        vrx = x.violacion_restricciones(self)
        vry = y.violacion_restricciones(self)
        
        if vrx == vry == 0:
            #x, y factibles
            return self.dominado(x,y)
        elif vrx == 0:
            #x factible, y no factible
            return 1
        elif vry == 0:
            #x no factible, y factible
            return -1
        else:
            if vrx < vry:
                return 1
            elif vrx == vry:
                return 0
            else:
                return -1
            
class Params(dict):
    '''Todos los parámetros que tengamos que pasar los pasamos aquí'''
    pass