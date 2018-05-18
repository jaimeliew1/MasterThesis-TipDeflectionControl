# -*- coding: utf-8 -*-
"""
Make plots for Tip Trajectory Tracking Chapter.
@author: J
"""

import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
import importlib, os


FigDir = '../Figures/Chapter_TipTrajectory/'
if not os.path.isdir(FigDir):
    os.makedirs(FigDir)


figScripts = [x[:-3] for x in os.listdir('../Postprocessing') if 'Ch3_' in x]

dlc_noipc = PostProc.DLC('dlc11_0')
dlc = PostProc.DLC('dlc11_1')
dlc2 = PostProc.DLC('dlc11_3')

plt.rc('text', usetex=True)
for script in figScripts:
    module = importlib.import_module('Postprocessing.' + script)
    module.run(dlc_noipc, dlc, dlc2, SAVE = FigDir + script + '.png')
plt.rc('text', usetex=False)



