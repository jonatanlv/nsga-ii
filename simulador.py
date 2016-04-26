# -*- coding: utf-8 -*-
"""
Batería de simulaciones:
Las simulaciones se definen por los siguientes parámetros:
test: definición del problema (dimensiones, límites, objetivos, frente de pareto)
init_pop_size: tamaño inicial de la población
pop_size: tamaño de la población
gens: generaciones

cruzador: operador evolutivo de cruce
mutador: operador evolutivo de mutación
selector: operador evolutivo de selección para cruce
seleccionador: operador evolutivo de selección natural

ruta_base: ruta base donde dejar todos los archivos generados por la simulación.
    La ruta final será:
    rutabase + / + test + / + pop_size.gens.nombres_operadores + / + fechasimulacion
nom_stats: nombre de las estadísticas
"""
import importlib
import representacion as rep
import metricas
import os
import datetime
import timeit
import Estadisticas
import numpy as np
import simulaciones as sims
import sys
import explorador

import logging

#simulación de juguete para probar
toy_sim = sims.szdt5.copy()
toy_sim.update({
    'init_pop_size':   50,
    'pop_size':        10,
    'gens':            20,
    'dibujar':         [5, True]
    }
    )

toy_sim2 = sims.simulaciones[0].copy()
toy_sim2.update({
    'test':            'ZDT1',
    'init_pop_size':   50,
    'pop_size':        10,
    'gens':            20,
    'dibujar':         [5, True],
    'nom_cruzador':    'uc',
    'cruzador':        rep.uniform_crossover,
    'nom_mutador':     'm1',
    'mutador':         rep.mutador1,
    'nom_selector':    'su',
    'selector':        rep.seleccion_uniforme,
    'nom_seleccionador':   'none',
    'seleccionador':   None
    })

def simular(sim):
    
    #Semilla para el generador de números aleatorios
    if 'seed' in sim:
        semilla = sim['seed']
    else:
        semilla = np.random.randint(2**30)
        
    np.random.seed(semilla)
    
    crono = timeit.time.time
    
    test = importlib.import_module(sim['test'])
    
    pr = test.construir_problema(**sim)
    
    tiempo_inicial = crono()
    pr.stats.nuevo_Acumulador('time')
    pr.stats['seed'] = semilla
    
    #Incluimos todos los parámetros de la simulación en las estadísticas
    for k, v in sim.items():
        pr.stats['param:' + k] = repr(v)
    
    rutasim = os.path.join(sim['ruta_base'], sim['test'], str(sim['pop_size']) + '.' + str(sim['gens']) + '.' +\
    sim['nom_mutador'] + '.' + sim['nom_cruzador'] + '.' + sim['nom_selector'] + '.' + sim['nom_seleccionador'],\
    datetime.datetime.now().strftime("%Y.%m.%d.%H.%M"))
    rutasim = os.path.abspath(rutasim)
    
    if not os.path.exists(rutasim):
        os.makedirs(rutasim)
    
    logging.basicConfig(level = sim['log_level'], filename = os.path.join(rutasim, 'ejecucion.log'), mode = 'w')    
    
    pop = rep.Poblacion(size = sim['pop_size'], operadores = sim, stats = pr.stats)
    gens = pr.stats.get_item('gens') #Las generaciones las llevamos aparte
    #Creamos un punto para poner los operadores y no hacerlo en todos
    rep.Punto(dimensiones = 1, operadores = sim, dist_fenotipo = pr.parametros.get('dist_fenotipo', None), **pr.extras)
    
    #Inicializamos la población
    logging.debug('Población inicial')
    for i in range(sim['init_pop_size']):
        p = rep.Punto(dimensiones = pr.dims, **pr.extras)
        p.rand(pr)
        pop.append(p)
    
    #Reducimos la población para entrar en el bucle principal
    pop.fast_non_dominated_sort(pr)
    elite, rango = [], 1
    while len(elite) < pop.size:
        frente = pop.select_with('rgo', rango)
        if frente != []:
            rep.crowding_distance_assignment(frente, pr)
            if len(elite) + len(frente) < pop.size:
                logging.debug('Inicio: Añadidos {} con rango {}'.format(len(frente), rango))
                elite.extend(frente)
            else:
                logging.debug('Inicio: Seleccionando del frente con rango {}'.format(rango))
                #rep.crowding_distance_assignment(frente, pr)
                logging.debug('Inicio: - Añadidos {} con rango {}'.format(pop.size - len(elite), rango))
                list.sort(frente, key = lambda x: x.crwd, reverse = True)
                elite.extend(frente[:(pop.size - len(elite))])
        rango += 1
    
    pop.clear()
    pop.extend(elite)
        
    #TODO se podrían usar otros criterios de parada y parametrizarlos
    while gens.value() < sim['gens']:
        tiempo_parcial = crono()
        if gens.value() % 5 == 0:
            if gens.value() % 50 == 0:
                print('5', end = '')
            else:
                print('.', end = '')
        sys.stdout.flush()
        gens() # Avanzamos el contador de la generación
        logging.info('** Generación {} **'.format(gens.value()))
        
#        #Quitamos puntos duplicados
#        unicos = []
#        for p in pop:
#            incluir = True
#            for q in unicos:
#                if np.all(p == q):
#                    incluir = False
#            if incluir:
#                unicos.append(p)
#                
#        pop.clear()
#        pop.extend(unicos)
        
        #Generamos la siguiente generación
        logging.debug('Generando offspring')
        offspring = []
        while len(offspring) < pop.size:
            p1, p2 = pop.selector(pr), pop.selector(pr)
            
            offspring.extend(pop.cruzador(p1, p2, pr))
        
        #Mutamos todo
        logging.debug('Mutando')
        for p in offspring:
            p.mutar(pr)
            p.gen = gens.value #Con esto vamos a poder ver cómo se avanza
        
        if gens.value() % sim['dibujar'][0] == 0:
            Estadisticas.dibujaPoblacion(pop, pr, rutasim, gens.value(), offs = offspring)
        
        #Juntamos las dos poblaciones
        logging.debug('Unimos')
        pop.union(offspring)
        
        #Ordenamos por el rango
        logging.debug('Fast non-dominated sort')
        pop.fast_non_dominated_sort(pr)
        
        #Seleccionamos a los mejores
        logging.debug('Seleccionando élite')
        elite, rango = [], 1
        while len(elite) < pop.size:
            frente = pop.select_with('rgo', rango)
            if frente != []:
                rep.crowding_distance_assignment(frente, pr)
                if len(elite) + len(frente) < pop.size:
                    logging.debug('Añadidos {} con rango {}'.format(len(frente), rango))
                    elite.extend(frente)
                else:
                    logging.debug('Seleccionando del frente con rango {}'.format(rango))
                    #rep.crowding_distance_assignment(frente, pr)
                    logging.debug(' - Añadidos {} con rango {}'.format(pop.size - len(elite), rango))
                    list.sort(frente, key = lambda x: x.crwd, reverse = True)
                    elite.extend(frente[:(pop.size - len(elite))])
            rango += 1
        
        pr.stats['time'](crono() - tiempo_parcial)
        
        #Reemplazamos la población actual con la élite por torneo
        pop.clear()
        if pr.parametros['nom_seleccionador'] == 'none':
            logging.debug('Sustiticón por la élite')
            pop.extend(elite)
        else:
            logging.debug('Selección por torneo')
            for i in range(pop.size):
                #p = pop.seleccionador(elite, pr)
                pop.append(pop.seleccionador(elite, pr))
    
    #Nos quedamos con las soluciones no dominadas
    no_dominadas = []
    for p in pop:
        incluir = True
        for q in pop:
            if pr.dominadoC(q, p) == 1: #Si q domina a p
                incluir = False
        if incluir:
            no_dominadas.append(p)
        
    pop.clear()
    pop.extend(no_dominadas)
    
    #Quitamos puntos duplicados
    unicos = []
    for p in pop:
        incluir = True
        for q in unicos:
            if np.all(p == q):
                incluir = False
        if incluir:
            unicos.append(p)
    
    pop.clear()
    pop.extend(unicos)
    
    pr.stats['no_dominadas'] = len(pop)
    
    #Ordenamos la población para las métricas
    list.sort(pop, key=lambda x: x.evaluado_en(pr)[0], reverse = True)
    
    #Guardamos los resultados obtenidos
    for m in sim['metricas']:
        nom = m.__name__
        pr.stats[nom] = m(pop, pr)
    pr.stats['tiempo_total'] = crono() - tiempo_inicial
    
    pr.stats.guardar(rutasim)
    
    Estadisticas.guardarPoblacion(pop, pr, ruta = rutasim, fichero = 'solucionFinal.txt')
    Estadisticas.guardarPoblacion(pop, pr, ruta = rutasim, fichero = 'poblacionFinal.txt', guardar = 'pop')
    
    if sim['dibujar'][1]:
        Estadisticas.dibujaPoblacion(pop, pr, rutasim, gens.value())
    
    #Cerramos el log para que en la siguiente ejecución se escriba en otro fichero
    logger = logging.getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])    
    
    return pop
    
def simularTodo(simulaciones):
    for sim in simulaciones:
        for i in range(sim['reps']):
            print('\n{:<40s} Iteración {}'.format(nombreSim(sim), i))
            simular(sim)
    print('\n\tSimulación finalizada')
    explorador.generar_estadisticas()
    print('\tEstadísticas finalizadas')
    
def nombreSim(sim):
    return sim['test'] + '.' + str(sim['pop_size']) + '.' + str(sim['gens']) + '.' +\
    sim['nom_mutador'] + '.' + sim['nom_cruzador'] + '.' + sim['nom_selector'] + '.' + sim['nom_seleccionador']