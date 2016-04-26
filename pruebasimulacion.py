# -*- coding: utf-8 -*-
"""
Prueba de una simulación
"""
#import ZDT1 as test
import ZDT3 as test
import representacion as rep
from Estadisticas import *

import timeit

import logging

logging.basicConfig(level=logging.DEBUG, filename = 'ejecucion.log', filemode = 'w')

ti = tp = timeit.time.time()
    
#Definimos los operadores evolutivos que vamos a usar
evops = {'mutador':         rep.mutador1,
         'cruzador':        rep.uniform_crossover,
         'selector':        rep.seleccion_uniforme,
         'seleccionador':   None
        }

#Formamos la población inicial aleatoria
logging.debug('Cargando población inicial')
test.problema.evops = evops
pop = rep.Poblacion(100, operadores=evops)
for i in range(250):
    p = rep.Punto(dimensiones = test.problema.dims, operadores = evops)
    p.rand(test.problema)
    pop.append(p)
    
dibujaPoblacion(pop, test.problema, 0)

#Número de generaciones
for i in range(200):
    #Generamos nueva generación
    print('Estamos en la generación {}'.format(i))
    logging.info('Generando siguiente generación: {}'.format(i+2))
    logging.debug('time:{}/{}'.format(timeit.time.time() - ti, timeit.time.time() - tp))
    tp = timeit.time.time()
    offspring = []
    while len(offspring) < pop.size:
        hijo, hija = pop.cruzador(pop.selector(test.problema), pop.selector(test.problema), test.problema)
        
        offspring.extend((hijo, hija))
        
    #mutamos todo
    logging.debug(' - Mutando')
    for p in offspring:
        p.mutar(test.problema)
        
    dibujaPoblacion(pop, test.problema, i + 1, offs = offspring)
            
    #juntamos con la nueva generacion
    logging.debug(' - Unimos todo')
    pop.union(offspring)
    
    #asignamos rango
    logging.debug(' - Fast non-dominated sort')
    pop.fast_non_dominated_sort(test.problema)
    
    elite = []
    rango = 1
    logging.debug(' - Seleccionando élite:')
    while len(elite) < pop.size and rango < pop.size * 2 + 1:
        frente = pop.select_with('rgo', rango)
        if len(elite) + len(frente) < pop.size:
            logging.debug(' -  - Añadidos {} con rango {}'.format(len(frente), rango))
            elite.extend(frente)
        else:
            logging.debug(' -  - Ordenando el frente con rango {}'.format(rango))
            rep.crowding_distance_assignment(frente, test.problema)
            logging.debug(' -  - Añadidos {} con rango {}'.format(pop.size - len(elite), rango))
            list.sort(frente, key = lambda x: x.crwd, reverse = True)
            elite.extend(frente[:(pop.size - len(elite))])
        rango += 1

    pop.clear()
    pop.union(elite)
    
dibujaPoblacion(pop, test.problema, i+1)