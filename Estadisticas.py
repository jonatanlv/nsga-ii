# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 19:53:26 2014

@author: jlaraval
"""
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

class Estadisticas(dict):
    def __init__(self, nombre):
        self.nombre = nombre
    
    def nuevo_Contador(self, nombre, acum = 0, cont = 0, paso = 1):
        self[nombre] = Contador(nombre, acum, cont, paso)
        return self[nombre]
    
    def nuevo_Acumulador(self, nombre, acum = None):
        self[nombre] = Acumulador(nombre, acum)
        return self[nombre]
            
    def getVal(self, nombre, default = None):
        return self.get(nombre).value()
        
    def get_item(self, nombre):
        return self[nombre]

    def guardar(self, ruta, fichero ='estadisticas.txt'):
        with open(os.path.join(ruta, fichero), mode='w') as f:
            for k, v in self.items():
                if isinstance(v, (Contador, Acumulador)):
                    linea = '{}\n'.format(repr(v))
                else:
                    linea = '{} = {}\n'.format(k, repr(v))
                f.write(linea)
                
class Contador():
    '''clase para contar cantidades'''
    def __init__(self, nombre, acum = 0, cont = 0, paso = 1):
        self.nombre = nombre
        self.acum = acum
        self.cont = cont
        self.paso = paso

    def value(self):
        return self.acum
    
    def getCont(self):
        return self.cont
        
    def media(self):
        if self.cont != 0:
            return self.acum / self.cont
        else:
            return 0
    
    def __call__(self, cantidad = None, paso = None):
        if cantidad is None:
            self.acum += self.paso
        else:
            self.acum += cantidad
        if paso is None:
            self.cont += self.paso
        else:
            self.cont += paso
    
    def __repr__(self):
        return 'Contador.{} = {} {}'.format(self.nombre, self.acum, self.cont)
        
class Acumulador():
    '''clase para acumular cantidades, para cuando es necesario recordar todos los valores'''
    def __init__(self, nombre, acum = None):
        self.nombre = nombre
        if acum is None:
            self.acum = []
        else:
            self.acum = acum

    def value(self):
        return self.acum
    
    def getCont(self):
        return len(self.acum)
        
    def media(self):
        return np.mean(self.acum)
        
    def stddev(self):
        return np.std(self.acum)
    
    def __call__(self, valor):
        self.acum.append(valor)
    
    def __repr__(self):
        salida = 'Acumulador.{} = {}\n'.format(self.nombre, str(self.acum))
        salida += 'Acumulador.{}.media = {}\n'.format(self.nombre, str(self.media()))
        salida += 'Acumulador.{}.stddev = {}'.format(self.nombre, str(self.stddev()))
        return salida

def dibujaPoblacion(pop, problema, ruta, gen, offs = None):
    
    logging.debug('Dibujando generación {}'.format(gen))
    xs = [p.evaluado_en(problema)[0] for p in pop]
    ys = [p.evaluado_en(problema)[1] for p in pop]
    
    xp = [p[0] for p in problema.fp['frente']]
    yp = [p[1] for p in problema.fp['frente']]
    
    tipo_fp = problema.parametros['grafica'].get('tipo_fp', 'k-.')
    tipo_s = problema.parametros['grafica'].get('tipo_s', 'r*')
    tipo_off = problema.parametros['grafica'].get('tipo_off', 'bx')
    
    plt.ioff()
    plt.figure()
    
    if offs is None:
        l1, l2 = plt.plot(xp, yp, tipo_fp, xs, ys, tipo_s)
        plt.legend((l1, l2), ('Frente de Pareto', 'Solución'))
        plt.title('Generación {}'.format(gen))
    else:
        xos = [p.evaluado_en(problema)[0] for p in offs]
        yos = [p.evaluado_en(problema)[1] for p in offs]
        
        l1, l3, l2 = plt.plot(xp, yp, tipo_fp, xos, yos, tipo_off, xs, ys, tipo_s)
        plt.legend((l1, l2, l3), ('Frente de Pareto', 'Solución', 'Offspring'))
        plt.title('Generación {} y offspring'.format(gen))
        
    plt.yscale(problema.parametros['grafica'].get('yscale', 'linear'))
    plt.xlim(*problema.parametros['grafica']['xlims'])
    plt.xlabel('$f_1$')
    plt.ylim(*problema.parametros['grafica']['ylims'])
    plt.ylabel('$f_2$')
    
    plt.savefig(os.path.join(ruta, 'figura{:03d}.png'.format(gen)), format='png', dpi=300)
    plt.close()

def guardarPoblacion(pop, problema, ruta, fichero, guardar='vals'):
    with open(os.path.join(ruta, fichero), mode='w') as f:
        for p in pop:
            if guardar == 'vals':
                res = str(p.evaluado_en(problema)).replace('\n', '')
            else:
                res = str(p).replace('\n', '')
            f.write('{}\n'.format(res))