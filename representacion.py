# -*- coding: utf-8 -*-
"""
Aquí vamos a meter todo lo relativo a la representación de las variables
de decisión así como la población (Punto, Poblacion, funciones de mutación, 
funciones de cruce, funciones de selección)
"""
import numpy as np
from Estadisticas import Estadisticas

class Punto(np.ndarray):
    '''Hereda de np.ndarray, representa una solución
    En los puntos tenemos la mutación
    Siempre vamos a considerar el propio punto como el genotipo
    '''
    def __new__(cls, dimensiones, initValue = None, rango = None, \
    operadores = None, crowded_distance = None, generacion = 1, dist_fenotipo = None, **kwargs):
        '''Para heredar de np.ndarray es necesario usar __new__ en lugar de __init__'''
        obj = np.ndarray.__new__(cls, dimensiones, **kwargs)
        obj.gen = generacion
        obj.vals = None
        obj.rest = None
        obj.rgo = rango
        obj.crwd = crowded_distance
        obj.np = 0
        obj.Sp = []
        '''Operadores es un diccionario de operadores evolutivos'''
        if not operadores is None:
            Punto._mutar = operadores['mutador']
            Punto._fenotipo = operadores['fenotipo']
        
        if not dist_fenotipo is None:
            Punto.dist_fenotipo = dist_fenotipo
        
        obj.setPunto(vector = initValue)
        
        return obj
        
    def setPunto(self, vector = None):
        if vector is None:
            self[:] = 0
        else:
            for i in range(len(self)):
                self[i] = vector[i]
    
    def copy(self, **kwargs):
        '''Devolvemos otro punto copia del actual'''
        p = Punto(dimensiones = len(self), **kwargs)
        p.gen = self.gen
        p.vals = self.vals
        p.rest = self.rest
        p.rgo = self.rgo
        p.crwd = self.crwd
        p.np = self.np
        p.Sp = self.Sp[:]
        
        p.setPunto(vector = self)
        
        return p
        
    
    def fenotipo(self):
        '''De momento trabajamos con representación real: fenotipo = genotipo'''
        return self.__class__._fenotipo(self)
    
    def rand(self, problema):
        if problema.parametros.get('tipo_var', 'real') == 'real':
            self[:] = (problema.lims[:, 1] - problema.lims[:, 0]) * np.random.rand(problema.dims) + problema.lims[:, 0]
        else:
            for i in range(problema.dims):
                self[i] = np.random.choice(problema.lims[i])
    
    def evaluado_en(self, problema):
        '''Evaluamos el punto con las funciones que nos da el problema'''
        if self.vals is None:
            self.vals = problema.evaluador(self)
        
        return self.vals
    
    def violacion_restricciones(self, problema):
        '''Calculamos el nivel de violación de las restricciones'''
        if self.rest is None:
            self.rest = problema.violacion_restricciones(self)
        
        return self.rest
        
    def mutar(self, problema):
        '''Con esta orden le pedimos al punto que se mute'''
        self.__class__._mutar(self, problema)

class Poblacion(list):
    '''La población será una lista de Puntos que representará a las soluciones
    En las poblaciones definimos el cruce y la selección'''
    def __init__(self, size, operadores, generacion = 0, stats = None):
        self.size = size
        self.gen = generacion
        
        if stats is None:
            self.stats = Estadisticas('Estadisticas')
        else:
            self.stats = stats            
        self.stats.nuevo_Contador('gens') #  Generación actual
        
        if not operadores is None:
            self.__class__._selector =        operadores['selector']
            self.__class__._cruzador =        operadores['cruzador']
            self.__class__._seleccionador =   operadores['seleccionador']
    
    def select_with(self, nomCaracteristica, valor):
        '''Seleccionamos los puntos con cierta caracteristica'''
        resultado = []
        for p in self:
            if p.__getattribute__(nomCaracteristica) == valor:
                resultado.append(p)
        
        return resultado
    
    def selector(self, problema):
        '''Seleccionamos para cruce'''
        return self.__class__._selector(self, problema)
    
    def cruzador(self, padre, madre, problema):
        '''Cruzamos dos puntos'''
        return self.__class__._cruzador(padre, madre, problema)
        
    def seleccionador(self, subpoblacion, problema):
        '''Seleccionamos de la población y quitamos los que no sirvan'''
        return self.__class__._seleccionador(self, subpoblacion, problema)
    
    def union(self, pop):
        for p in pop:
            self.append(p)
    
    def borrar(self, conjunto):
        for p in conjunto:
            if p in self:
                self.remove(p)
    
    def fast_non_dominated_sort(self, problema):
        '''Seguimos el algoritmo descrito en "A fast and elitist multiobjective GA: NSGA-II"'''
        #TODO: Este procedimiento se puede mejorar no teniendo que calcular el rango de toda la población
        frentes = [[]]
        for p in self:
            p.Sp, p.np = [], 0
            for q in self:
                dominio = problema.dominadoC(p, q)
                if dominio == 1: # p domina a q
                    p.Sp.append(q)
                elif dominio == -1: # q domina a p
                    p.np += 1
            if p.np == 0:
                p.rgo = 1
                frentes[0].append(p)
        
        i = 0
        while True:
            siguienteFrente = []
            for p in frentes[i]:
                for q in p.Sp:
                    q.np -= 1
                    if q.np == 0:
                        q.rgo = i + 2
                        siguienteFrente.append(q)
            if siguienteFrente == []:
                break
            frentes.append(siguienteFrente[:])
            i += 1
            
    def __contains__(self, item):
        for p in self:
            if p is item:
                return True
        return False
            
def crowding_distance_assignment(I, problema):
    '''Seguimos el algoritmo descrito en "A fast and elitist multiobjective GA: NSGA-II"'''
    I.sort(reverse = True, key = lambda x: x[0])
    extremos = [I[0], I[-1]]
    
    for p in I:
        p.crwd = 0
    for p in extremos:
        p.crwd = float('inf')
    
    #TODO No encuentro la manera de hacer esto con numpy
    objetivos = []
    for p in I:
        parcial = [p]
        parcial.extend(p.evaluado_en(problema))
        objetivos.append(parcial[:])
    
    # objetivos[i] = [p_i, f1(p_i), f2(p_i), ..., fn(p_i)]
    for i in range(1, len(problema.objetivos) + 1):
        objetivos.sort(key=lambda x: x[i])
        fmax = max(objetivos, key=lambda x: x[i])[i]
        fmin = min(objetivos, key=lambda x: x[i])[i]
        
        for j in range(1, len(objetivos) - 1):
            objetivos[j][0].crwd += (objetivos[j+1][i] - objetivos[j-1][i]) / (fmax - fmin)

############################################
# FENOTIPOS
# Siempre tienen la misma firma:
#     def nombre(punto)
# Devuelven
#     el fenotipo que le corresponde al punto
############################################
def real(punto):
    '''Representación real, fenotipo = genotipo'''
    return punto
    
def binario(punto):
    '''Representación binaria'''
    fenotipo = []
    for i in range(len(punto.dist_fenotipo)):
        li = np.sum(punto.dist_fenotipo[:i])
        ui = np.sum(punto.dist_fenotipo[:i + 1])
        
        fenotipo.append(punto[li:ui])
        
    return fenotipo

############################################
# OPERADORES DE MUTACIÓN
# Siempre tienen la misma firma:
#     def nombre(punto, problema)
############################################
def mutador1(punto, problema):
    '''Mutamos cualquier componente con probabilidad proporcional
    a la dimensión del espacio y esa componente puede tomar cualquier punto'''
    p = problema.parametros.get('pm', 1 / problema.dims)
    
    mascara = np.random.rand(problema.dims) < p
    punto[mascara] = (problema.lims[mascara, 1] - problema.lims[mascara, 0]) \
    * np.random.rand(mascara.sum()) + problema.lims[mascara, 0]
    
def mutadorb(punto, problema):
    '''Mutador de estados para variables discretas, se elige una componente
    y se fuerza a que cambie a alguno de los otros estados'''
    p = problema.parametros.get('pm', 1 / problema.dims)
    
    mascara = np.random.rand(problema.dims) < p
    for i in range(len(problema.lims)):
        if not mascara[i]:
            continue
        nvalor = np.random.choice(problema.lims[i])
        while nvalor == punto[i]:
            nvalor = np.random.choice(problema.lims[i])
        punto[i] = nvalor
    
def mutador_init(punto, problema):
    '''Escogemos un punto cualquiera del espacio de decisión'''
    punto.rand(problema)

def mutacion_aleatoria(punto, problema):
    '''Cada componente es variada uniformemente con el rango máximo que se le permita'''
    copy_lims = problema.lims.copy()
    copy_lims[:,0] = np.abs(copy_lims[:,0] - punto)
    copy_lims[:,1] = np.abs(copy_lims[:,1] - punto)
    deltas = np.min(copy_lims, axis = 1) #máxima variabilidad permitida en cada componente
    u = np.random.rand(problema.dims) * 2 - 1 # la variación que vamos a hacer en cada componente
    
    punto.setPunto(vector = punto + u * deltas)

def mutacion_polinomial(punto, problema):
    '''mutación polinomial'''
    p = problema.parametros.get('pm', 1 / problema.dims)
    eta = problema.parametros.get('mp', 2)
    
    for i in range(problema.dims):
        if np.random.rand() >= p:
            #No mutamos este gen
            continue

        u = np.random.rand()
        if u <= .5:
            delta = np.power(2 * u, 1 / (eta + 1)) - 1
            punto[i] += delta * (punto[i] - problema.lims[i,0])
        else:
            delta = 1 - np.power(2 * (1 - u), 1 / (eta + 1))
            punto[i] += delta * (problema.lims[i,1] - punto[i])

############################################
# GENERADORES DE CRUCES
# Siempre tienen la misma firma:
#     def nombre(seleccionParaCruce, cruzadorBasico)
# Devuelve una función con la siguiente firma
#     def $(poblacion, problema)
# que a su vez devolverá:
#     2 hijos
############################################
def generar_cruzador(selector, cruzador):
    def funcion(poblacion, problema):
        p1 = selector(poblacion, problema)
        p2 = selector(poblacion, problema)
        
        return cruzador(p1, p2, problema)
        
    return funcion

############################################
# CRUZADORES BÁSICOS
# Siempre tienen la misma firma:
#     def nombre(padre, madre, problema)
# Devuelven:
#     dos puntos soluciones
############################################
'''Cruces básicos'''
def line_recombination(padre, madre, problema):
    pass
    
def intermediate_recombination(padre, madre, problema):
    pass

def trivial(padre, madre, problema):
    '''Recombinador trivial: devuelve al padre y la madre'''
    return padre, madre

def blended_crossover(padre, madre, problema):
    '''blended crossover BLX-alpha'''
    '''uniform compound recombination'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    alpha = problema.parametros.get('blx', .5)
    
    for i in range(problema.dims):
        alpha = problema.parametros.get('blx', .5)
        
        entrar = True
        while entrar:
            factor = np.random.rand() * (1 + 2 * alpha) - alpha
            
            hijo[i] = (1 - factor) * padre[i] + factor * madre[i]
            hija[i] = factor * padre[i] + (1 - factor) * madre[i]
            
            if problema.lims[i, 0] <= hijo[i] <= problema.lims[i, 1] and\
                problema.lims[i, 0] <= hija[i] <= problema.lims[i, 1]:
                entrar = False
            else:
                alpha = alpha / 2
                #print('padre {}, madre {}, alpha = {}'.format(str(padre), str(madre), alpha))
    
    return hijo, hija

def simulated_binary_crossover2(padre, madre, problema):
    '''simulated binary crossover'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    n = problema.parametros.get('sbx', 2)
    
    for i in range(problema.dims):
        #Lo hacemos componente a componente para evitar sacar muchos valores
        y1, y2 = min(padre[i], madre[i]), max(padre[i], madre[i])
        yl, yu = problema.lims[i,0], problema.lims[i,1]
        
        if np.abs(y2 - y1) > problema.parametros.get('sbx_prec', 10**-6):
            u = np.random.rand()
            
            beta = 1 + 2 * (y1 - yl) / (y2 - y1)
            alpha = 2 - np.power(beta, -(n + 1))
            if u <= 1 / alpha:
                betaq = np.power(u * alpha, 1 / (n + 1))
            else:
                betaq = np.power(1 / (2 - u * alpha), 1 / (n + 1))
                
            h1 = .5 * ( y1 + y2 - betaq * (y2 - y1))
                    
            beta = 1 + 2 * (yu - y2) / (y2 - y1)
            alpha = 2 - np.power(beta, -(n + 1))
            if u <= 1 / alpha:
                betaq = np.power(u * alpha, 1 / (n + 1))
            else:
                betaq = np.power(1 / (2 - u * alpha), 1 / (n + 1))
                
            h2 =  .5 * ( y1 + y2 - betaq * (y2 - y1))
            
            if h1 < yl:
                h1 = yl
            elif h1 > yu:
                h1 = yu
                
            if h2 < yl:
                h2 = yl
            elif h2 > yu:
                h2 = yu
            
            if np.random.rand() < .5:
                hijo[i] = h1
                hija[i] = h2
            else:
                hijo[i] = h2
                hija[i] = h1
    
    return hijo, hija
    
def simulated_binary_crossover(padre, madre, problema):
    '''simulated binary crossover'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    n = problema.parametros.get('sbx', 2)
    
    for i in range(problema.dims):
        #Lo hacemos componente a componente para evitar sacar muchos valores
        
        u = np.random.rand()
            
        if u < .5:
            beta = np.power(2*u, 1/ (n + 1))
        else:
            beta = np.power(1 / (2 - 2 * u), 1 / (n + 1))
        
        hijo[i] = .5 * (padre[i] + madre[i]) + .5 * beta * (padre[i] - madre[i])
        hija[i] = .5 * (padre[i] + madre[i]) - .5 * beta * (padre[i] - madre[i])
        
        if hijo[i] < problema.lims[i, 0]:
            hijo[i] = problema.lims[i, 0]
        elif hijo[i] > problema.lims[i, 1]:
            hijo[i] = problema.lims[i, 1]
        
        if hija[i] < problema.lims[i, 0]:
            hija[i] = problema.lims[i, 0]
        elif hija[i] > problema.lims[i, 1]:
            hija[i] = problema.lims[i, 1]
    
    return hijo, hija

def uniform_compound_recombination(padre, madre, problema):
    '''uniform compound recombination'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    if 'ucr' in problema.parametros:
        c = problema.parametros['ucr']
    else:
        c = -0.75
    
    sw = None
    
    while sw is None or not (problema.en_el_dominio(hijo) and problema.en_el_dominio(hija)):
        sw = True
        
        #factor son los factores por cada componente vs ~ U[-1, 1]
        vs = np.random.rand(problema.dims) * 2 - 1
        factor = vs * np.abs(vs) ** c  + .5
        
        hijo.setPunto(vector = factor * padre + (1 - factor) * madre)
        hija.setPunto(vector = (1 - factor) * padre + factor * madre)
    
    return hijo, hija

def one_point_crossover(padre, madre, problema):
    '''one point crossover'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    cut = None
    
    while cut is None or not (problema.en_el_dominio(hijo) and problema.en_el_dominio(hija)):
        cut = np.random.randint(problema.dims)
    
        hijo[:cut] = padre[:cut]
        hijo[cut:] = madre[cut:]
        
        hija[cut:] = padre[cut:]
        hija[:cut] = madre[:cut]
    
    return hijo, hija
    
def two_point_crossover(padre, madre, problema):
    '''two point crossover'''
    
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
    
    cut1 = None
    
    while cut1 is None or not (problema.en_el_dominio(hijo) and problema.en_el_dominio(hija)):
        cut1 = np.random.randint(problema.dims - 1)
        cut2 = np.random.randint(cut1, problema.dims)
    
        hijo[:cut1] = padre[:cut1]
        hijo[cut1:cut2] = madre[cut1:cut2]
        hijo[cut2:] = padre[cut2:]
        
        hija[:cut1] = madre[:cut1]
        hija[cut1:cut2] = padre[cut1:cut2]
        hija[cut2:] = madre[cut2:]
    
    return hijo, hija

def uniform_crossover(padre, madre, problema):
    '''uniform crossover, naive para representaciones reales'''
    hijo = Punto(dimensiones = problema.dims, **problema.extras)
    hija = Punto(dimensiones = problema.dims, **problema.extras)
        
    cut = None
    
    while cut is None or not (problema.en_el_dominio(hijo) and problema.en_el_dominio(hija)):
        cut = np.random.rand(problema.dims)
        
        cut1 = (cut <= .5)
        cut2 = (cut > .5)
        
        hijo[cut2] = padre[cut2]
        hijo[cut1] = madre[cut1]
    
        hija[cut1] = padre[cut1]
        hija[cut2] = madre[cut2]
    
    return hijo, hija

############################################
# OPERADORES DE SELECCION
# Siempre tienen la misma firma:
#     def nombre(poblacion, subpoblacion, problema)
# Devuelve
#     Un punto de la población
############################################
'''Dada la población seleccionamos los más aptos'''
def noneSelect(poblacion, subpoblacion, problema):
    '''No selecciona, va devolviendo los puntos de subpoblación en orden'''
    i = 0
    while True:
        yield subpoblacion[i]
        i = (i + 1) % len(subpoblacion)

def ns_tournament_selection_sparsity(poblacion, subpoblacion, problema):
    '''Non-dominated sorting lexicographic tournament with sparsity'''
    t = problema.parametros.get('t_size', 2) #Tamaño del torneo
    p1 = seleccion_uniforme(subpoblacion, problema)
    best = p1.copy(**problema.extras)
    
    for i in range(t-1):
        p2 = seleccion_uniforme(subpoblacion, problema)
        if p2.rgo < p1.rgo:
            best = p2
        elif best.rgo == p2.rgo:
            if p2.crwd > best.crwd:
                best = p2
    
    return best
    
def ns_tournament_selection_sparsity_constraint(poblacion, subpoblacion, problema):
    '''Non-dominated sorting lexicographic tournament with sparsity and restrictions'''
    t = problema.parametros.get('t_size', 2)
    p1 = seleccion_uniforme(subpoblacion, problema)
    best = p1.copy(**problema.extras)
    
    for i in range(t-1):
        p2 = seleccion_uniforme(subpoblacion, problema)
        if best.violacion_restricciones(problema) == p2.violacion_restricciones(problema) == 0:
            #Si los dos cumplen todas las restricciones el criterio normal
            if p2.rgo < best.rgo:
                best = p2
            elif best.rgo == p2.rgo:
                if p2.crwd > best.crwd:
                    best = p2
        elif best.violacion_restricciones(problema) == 0:
            #p1 cumple las restricciones y p2 no
            continue
        elif p2.violacion_restricciones(problema) == 0:
            #p2 cumple las restricciones y p1 no
            best = p2
        else:
            #ni p1 ni p2 cumplen las restricciones
            if best.violacion_restricciones(problema) > p2.violacion_restricciones(problema):
                #mayor violación por parte de p1
                best = p2
            elif best.violacion_restricciones(problema) == p2.violacion_restricciones(problema):
                #escogemos al azar
                if np.random.rand() < .5:
                    best = p2
            
    return best

############################################
# OPERADORES DE SELECCION PARA CRUCE
# Siempre tienen la misma firma:
#     def nombre(poblacion, problema)
# Devuelve:
#     un punto de la población
############################################
'''Dada la población seleccionamos los candidatos a cruzarse'''
def seleccion_uniforme(poblacion, problema):
    return poblacion[np.random.randint(problema.parametros['pop_size'])]
    
def selector(seleccionador):
    '''Convertimos un seleccionador en un selector'''
    def f(poblacion, problema):
        return seleccionador(poblacion, poblacion, problema)
        
    return f
