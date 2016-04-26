# -*- coding: utf-8 -*-
"""
Simulaciones
"""
import representacion as rep
import os
import logging
import metricas

'''Opciones que se van a usar'''
globales = {
    'grafica':          {'xlims':(0,1), 'ylims':(0,4)},
    'reps':             5
    }

base = [
    {
    'test':             'ZDT1',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250
    },
    {
    'test':             'ZDT2',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250
    },
    {
    'test':             'ZDT3',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250,
    'grafica':          {'xlims':(0,1), 'ylims':(-1,3), 'tipo_fp':'k.'}
    },
    {
    'test':             'ZDT4',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250
    },
    {
    'test':             'ZDT6',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250
    }
    ]

operadores = [
    {
    'nom_cruzador':     'uc',
    'cruzador':         rep.uniform_crossover,
    'nom_mutador':      'm1',
    'mutador':          rep.mutador1,
    'nom_selector':     'su',
    'selector':         rep.seleccion_uniforme,
    'nom_seleccionador':   'none',
    'seleccionador':    rep.noneSelect,
    'fenotipo':         rep.real
    },
    {
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              2,
    'nom_mutador':      'm1',
    'mutador':          rep.mutador1,
    'nom_selector':     'su',
    'selector':         rep.seleccion_uniforme,
    'nom_seleccionador':   'none',
    'seleccionador':    rep.noneSelect,
    'fenotipo':         rep.real
    },
    {
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              2,
    'nom_mutador':      'ma',
    'mutador':          rep.mutacion_aleatoria,
    'nom_selector':     'su',
    'selector':         rep.seleccion_uniforme,
    'nom_seleccionador':   'nstss',
    'seleccionador':    rep.ns_tournament_selection_sparsity,
    't_size':           2,
    'fenotipo':         rep.real
    },
    {
    'nom_cruzador':     'blx',
    'cruzador':         rep.blended_crossover,
    'blx':              .5,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               2,
    'nom_selector':     'su',
    'selector':         rep.seleccion_uniforme,
    'nom_seleccionador':   'nstss',
    'seleccionador':    rep.ns_tournament_selection_sparsity,
    't_size':           2,
    'fenotipo':         rep.real
    },
    {
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              2,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               100,
    'nom_selector':     'su',
    'selector':         rep.seleccion_uniforme,
    'nom_seleccionador':   'nstss',
    'seleccionador':    rep.ns_tournament_selection_sparsity,
    't_size':           2,
    'fenotipo':         rep.real
    },
    {
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              2,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               10,
    'nom_selector':     'nstss',
    'selector':         rep.selector(rep.ns_tournament_selection_sparsity),
    'nom_seleccionador':   'none',
    'seleccionador':    None,
    't_size':           2,
    'fenotipo':         rep.real
    }
    ]

estadisticas = [
    {
    'ruta_base':        '.' + os.path.sep + 'ejecuciones',
    'nom_stats':        'stats',
    'log_level':        logging.DEBUG,
    'dibujar':          [10, True],
    'metricas':         [metricas.Lambda, metricas.Spread, metricas.Upsilon]
    }
    ]

''' Todas las posibles configuraciones de los diccionarios anteriores
serán las simulaciones a realizar '''
simulaciones = [dict(list(globales.items()) + list(o.items()) + list(e.items()) + list(b.items()))\
    for e in estadisticas for o in operadores for b in base]
        
''' Simulaciones específicas '''
szdt1 = dict(list(globales.items()) + list(base[0].items()) + list(operadores[5].items()) + list(estadisticas[0].items()))

szdt2 = dict(list(globales.items()) + list(base[1].items()) + list(operadores[5].items()) + list(estadisticas[0].items()))

szdt3 = dict(list(globales.items()) + list(base[2].items()) + list(operadores[5].items()) + list(estadisticas[0].items()))

szdt4 = dict(list(globales.items()) + list(base[3].items()) + list(operadores[5].items()) + list(estadisticas[0].items()))

szdt6 = dict(list(globales.items()) + list(base[4].items()) + list(operadores[5].items()) + list(estadisticas[0].items()))

szdt5 = {
    'reps':             5,
    'test':             'ZDT5',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250,
    'pm':               .5,
    'nom_mutador':      'mb',
    'mutador':          rep.mutadorb,
    'nom_cruzador':     'uc',
    'cruzador':         rep.uniform_crossover,
    'nom_seleccionador':   'none',
    'seleccionador':    None,
    'nom_selector':     'nstss',
    'selector':         rep.selector(rep.ns_tournament_selection_sparsity),
    'fenotipo':         rep.binario,
    'grafica':          {'xlims':(0,32), 'ylims':(0,100), 'yscale': 'log', 'tipo_fp': 'k+'},
    'ruta_base':        '.' + os.path.sep + 'ejecuciones',
    'nom_stats':        'stats',
    'log_level':        logging.DEBUG,
    'dibujar':          [10, True],
    'metricas':         [metricas.Lambda, metricas.Spread, metricas.Upsilon]
    }
    
sconstr = {
    'reps':             5,
    'test':             'CONSTR',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250,
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              20,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               100,
    'nom_selector':     'nstssc',
    'selector':         rep.selector(rep.ns_tournament_selection_sparsity_constraint),
    'nom_seleccionador':   'none',
    'seleccionador':    None,
    't_size':           2,
    'fenotipo':         rep.real,
    'grafica':          {'xlims':(0,1), 'ylims':(0,10), 'tipo_fp': 'k-.'},
    'ruta_base':        '.' + os.path.sep + 'ejecuciones',
    'nom_stats':        'stats',
    'log_level':        logging.DEBUG,
    'dibujar':          [10, True],
    'metricas':         [metricas.Lambda, metricas.Spread, metricas.Upsilon]
    }


ssrn = {
    'reps':             5,
    'test':             'SRN',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250,
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              20,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               100,
    'nom_selector':     'nstssc',
    'selector':         rep.selector(rep.ns_tournament_selection_sparsity_constraint),
    'nom_seleccionador':   'none',
    'seleccionador':    None,
    't_size':           2,
    'fenotipo':         rep.real,
    'grafica':          {'xlims':(0,250), 'ylims':(-250,50), 'tipo_fp': 'k.'},
    'ruta_base':        '.' + os.path.sep + 'ejecuciones',
    'nom_stats':        'stats',
    'log_level':        logging.DEBUG,
    'dibujar':          [10, True],
    'metricas':         [metricas.Lambda, metricas.Spread, metricas.Upsilon]
    }
    
stnk = {
    'reps':             5,
    'test':             'TNK',
    'init_pop_size':    250,
    'pop_size':         100,
    'gens':             250,
    'nom_cruzador':     'sbx',
    'cruzador':         rep.simulated_binary_crossover,
    'sbx':              20,
    'nom_mutador':      'mp',
    'mutador':          rep.mutacion_polinomial,
    'mp':               100,
    'nom_selector':     'nstssc',
    'selector':         rep.selector(rep.ns_tournament_selection_sparsity_constraint),
    'nom_seleccionador':   'none',
    'seleccionador':    None,
    't_size':           2,
    'fenotipo':         rep.real,
    'grafica':          {'xlims':(0,1.4), 'ylims':(0,1.4), 'tipo_fp': 'k.'},
    'ruta_base':        '.' + os.path.sep + 'ejecuciones',
    'nom_stats':        'stats',
    'log_level':        logging.DEBUG,
    'dibujar':          [10, True],
    'metricas':         [metricas.Lambda, metricas.Spread, metricas.Upsilon]
    }

# Para probar que todo va bien, podemos ejecutar con opciones reducidas y guardando aparte
toyficar = {
    'ruta_base':        '.' + os.path.sep + 'toy',
    'init_pop_size':    100,
    'pop_size':         30,
    'gens':             50,
    'dibujar':          [5, True]
    
}

esta_noche = [szdt1, szdt2, szdt3, szdt4, szdt5, szdt6, stnk, sconstr, ssrn]