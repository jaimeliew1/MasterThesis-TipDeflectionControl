# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:36:45 2018

@author: J
"""

import numpy as np
from Modelling import BladeModel

BS = ['b_1', 'b_2', 'b_3', 'b_4' ]
AS = ['a_2', 'a_3', 'a_4', 'a_5']

temp = ''' \\rule{0pt}{4ex}  wsp & \\( \\frac{b_1s^3 + b_2s^2 + b_3s + b_4}{s^4 + a_2s^3 + a_3s^2 + a_4s + a_5} \\)  \\\\ \\hline'''
WSP = np.arange(4, 27, 2)
models = BladeModel.make()


for m in models:
    s = temp
    toreplace = dict(zip(BS, [f'{x:2.4f}' for x in m.b]))

    s = s.replace('wsp', str(m.wsp))
    for x, y in toreplace.items():
        s = s.replace(x, y)

    toreplace = dict(zip(AS, [f'{x:2.4f}' for x in m.a[1:]]))
    for x, y in toreplace.items():
        s = s.replace(x, y)
    print(s)

