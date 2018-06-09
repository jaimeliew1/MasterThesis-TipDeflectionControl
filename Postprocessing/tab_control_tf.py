# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 18:43:14 2018

@author: J
"""
from Modelling import BladeModel
from importlib import import_module
from JaimesThesisModule import ControlDesign


Modules = ['IPC_PI',
           'IPC04',
           'IPC09',
           'IPC10',
           'IPC11',
           'IPC07',]


X = [{}]*6
P = BladeModel.Blade(wsp=18)
for i, mod_name in enumerate(Modules):
    module = import_module('Controllers.' + mod_name)
    C = module.make()
    sys = ControlDesign.Turbine(P, C)
    print(C.num)