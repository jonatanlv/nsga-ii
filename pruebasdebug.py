# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:37:18 2014

@author: jlaraval
"""
import simulaciones as s
import ZDT1 as test
import representacion as rep
import Estadisticas as st

sim = s.szdt1
pr = test.construir_problema(**sim)
pop = rep.Poblacion(size = sim['pop_size'], operadores = sim, stats = pr.stats)
rep.Punto(dimensiones = 1, operadores = sim, dist_fenotipo = None, **pr.extras)

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
            elite.extend(frente)
        else:
            #rep.crowding_distance_assignment(frente, pr)
            list.sort(frente, key = lambda x: x.crwd, reverse = True)
            elite.extend(frente[:(pop.size - len(elite))])
    rango += 1

pop.clear()
pop.extend(elite)

#pr.parametros['grafica'].update(dict(xlims = (0,1), ylims = (90,250), yscale = 'log'))

offspring = []
while len(offspring) < pop.size:
    p1, p2 = pop.selector(pr), pop.selector(pr)
    
    offspring.extend(pop.cruzador(p1, p2, pr))
    
for p in offspring:
    p.mutar(pr)
    
pop.union(offspring)

pop.fast_non_dominated_sort(pr)

elite, rango = [], 1
while len(elite) < pop.size:
    frente = pop.select_with('rgo', rango)
    if frente != []:
        rep.crowding_distance_assignment(frente, pr)
        if len(elite) + len(frente) < pop.size:
            elite.extend(frente)
        else:
            list.sort(frente, key = lambda x: x.crwd, reverse = True)
            elite.extend(frente[:(pop.size - len(elite))])
    rango += 1

pop.clear()
pop.extend(elite)
#for i in range(pop.size):
#    #pop.seleccionador(elite, pr)
#    pop.append(pop.seleccionador(elite, pr))

#st.dibujaPoblacion(pop, pr, '.', 0, offs = elite)
