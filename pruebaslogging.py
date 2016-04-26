# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 22:07:17 2014

@author: jlaraval
"""

import os
import logging

def f(subcarpeta):
    fichero = os.path.join('.', subcarpeta)
    
    os.mkdir(fichero)
    
    logging.basicConfig(level = logging.DEBUG, filename = os.path.join(fichero, 'ejecucion.log')\
    , filemode = 'w')
    
    logging.warn(subcarpeta)
    logging.debug(subcarpeta)
    
    logging.handlers[0].close()