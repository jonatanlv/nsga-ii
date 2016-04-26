# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 23:23:23 2014

@author: jlaraval
"""

class A():
    def __init__(self, method):
        self._method = method
        
    def method(self, param):
        return self._method(param)
        

def metodo(x):
    print(x)