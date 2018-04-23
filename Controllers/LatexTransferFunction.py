# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:46:49 2018

@author: J
"""
import numpy as np
from Controllers.Discretisation import discretise
from IPC04 import make

Fs = 100
C = make()
Cd = discretise(C, Fs=Fs)

# Continuous transfer function
Nnum = len(C.num)
Nden = len(C.den)

Ca = '$$C_a = \\frac{'
for i, b in enumerate(C.num):
    if i != Nnum - 1:
        Ca += '{:2.4f}s^{} + '.format(b, Nnum - i - 1)
    else:
        Ca += '{:2.4f}'.format(b)
Ca += '}{'

for i, a in enumerate(C.den):
    if i == 0:
        Ca += 's^{} + '.format(Nden - i - 1)
    elif i != Nden - 1:
        Ca += '{:2.4f}s^{} + '.format(a, Nden - i - 1)
    else:
        Ca += '{:2.4f}'.format(a)
Ca += '}$$'
print(Ca)


# Discrete transfer function
Nnum = len(Cd.num)
Nden = len(Cd.den)

Ca = '$$C_d = \\frac{'
for i, b in enumerate(Cd.num):
    thisb = '{:2.4e}'.format(b)
    thisb = thisb.replace('e', '\\times 10^{') + '}'
    thisb = thisb.replace('-0', '-')

    if i==0:
        Ca += '{}z^{}'.format(thisb, Nnum - i - 1)
    elif i != Nnum - 1:
        if b>0:
            Ca += '+{}z^{}'.format(thisb, Nnum - i - 1)
        else:
            Ca += '{}z^{}  '.format(thisb, Nnum - i - 1)
    else:
        if b>0:
            Ca += '+{}'.format(thisb)
        else:
            Ca +='{}'.format(thisb)
Ca += '}{'

for i, a in enumerate(Cd.den):
    if i == 0:
        Ca += 'z^{}'.format(Nden - i - 1)
    elif i != Nden - 1:
        if a > 0:
            Ca += '+ {:2.4f}z^{}'.format(a, Nden - i - 1)
        else:
            Ca += '{:2.4f}z^{}'.format(a, Nden - i - 1)
    else:
        if a > 0:
            Ca += '+ {:2.4f}'.format(a)
        else:
            Ca += '{:2.4f}'.format(a)
Ca += '}$$'
print(Ca)

#%% Difference equation

diffEq = '\\begin{multiline}\ny[k] = '
for i, b in enumerate(Cd.num):
    thisb = '{:+2.2e}'.format(b)
    thisb = thisb.replace('e', '\\times 10^{') + '}'
    thisb = thisb.replace('-0', '-')
    if i == 0:
        diffEq += thisb.replace('+','')
        diffEq += 'x[k]'
    else:
        diffEq += thisb
        diffEq += 'x[k-{}]'.format(i)

diffEq += '\\\\'

for i, a in enumerate(Cd.den):
    thisa = '{:+2.2f}'.format(-a)
    if i == 0:
        pass
    else:
        diffEq += thisa
        diffEq += 'y[k-{}]'.format(i)
diffEq += '\n\\end{multiline}'
print(diffEq)