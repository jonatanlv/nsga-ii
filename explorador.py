# -*- coding: utf-8 -*-
"""
Para extraer estadisticas
"""
import os
import re
from Estadisticas import Estadisticas

def explorador(path = '.', niveles = float('inf'), **kwargs):
    '''Devuelve todos los archivos desde el actual profundizando niveles'''
    if niveles == 0:
        return [os.path.abspath(path)]
            
    res = []
    parcial = os.listdir(os.path.abspath(path))
    for r in parcial:
        ruta = os.path.abspath(os.path.join(path, r))
        if os.path.isdir(ruta):
            res.extend(explorador(path = ruta, niveles = niveles - 1, **kwargs))
        else:
            res.append(ruta)
    
    return res
    
def filtro(lista, patron = '', excluidos = ''):
    p = re.compile(patron, re.IGNORECASE)
    q = re.compile(excluidos, re.IGNORECASE)
    if excluidos == '':
        return [l for l in lista if p.search(l)]
    else:
        return [l for l in lista if p.search(l) if not q.search(l)]

def ver(lista):
    for l in lista:
        print(l)
        
def lookup(lista, valor, default = 0):
    busqueda = filtro(lista, valor + ' = ')
    if len(busqueda) == 0:
        return default
    else:
        return float((busqueda[0]).split(' = ')[1])
    
def generar_estadisticas(ruta_base = '.'):
    valores = ['Lambda','Spread','Upsilon','no_dominadas']
    patrones_OK = [r'ejecuciones']
    patron_KO = r'ejecuciones\\antiguos'
    f_estadisticas = r'\\estadisticas.txt'
    
    lista = explorador(path = ruta_base, niveles = 3)
    lista_filtrada = []
    for patron in patrones_OK:
        parcial = filtro(lista, patron = patron, excluidos = patron_KO)
        for sub in parcial:
            if not sub in lista_filtrada:
                lista_filtrada.append(sub)
    
    #En este punto lista_filtrada contiene la ruta base de cada simulación.
    #Es decir, la ruta justo antes de la carpeta con la fecha
    for ruta in lista_filtrada:
        l_arch = explorador(ruta)
        fl_arch = filtro(l_arch, f_estadisticas)
        #Ahora tenemos que recorrer todos los fl_arch y sacar las estadísticas
        #Todos corresponden al mismo experimento
        nombre_sim = ruta[len(ruta) - ruta[::-1].find('\\'):]
        st = Estadisticas(nombre_sim)
        for v in valores:
            st.nuevo_Acumulador(v)
        
        for arch in fl_arch:
            #Leemos el archivo de estadísticas
            with open(arch) as fin:
                lectura = [l.strip() for l in fin]
            
            for v in valores:
                st[v](lookup(lectura, v))
            
            st.guardar(ruta, fichero = nombre_sim + '.txt')
    