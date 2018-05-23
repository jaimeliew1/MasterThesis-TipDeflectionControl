# -*- coding: utf-8 -*-
"""
Make plots for Theoretical Framework Chapter.
@author: J
"""

import matplotlib.pyplot as plt
import importlib, os


FigDir = '../Figures/Chapter_BladeModelling/'
if not os.path.isdir(FigDir):
    os.makedirs(FigDir)

figScripts = [x[:-3] for x in os.listdir('../Postprocessing') if 'Ch4_' in x]

plt.rc('text', usetex=True)
for script in figScripts:
    module = importlib.import_module('Postprocessing.' + script)
    module.run(SAVE = FigDir + script + '.png')
plt.rc('text', usetex=False)



