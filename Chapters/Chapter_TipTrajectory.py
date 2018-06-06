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

dlcs = {'dlc11_0':PostProc.DLC('dlc11_0'),
'dlc11_1':PostProc.DLC('dlc11_1'),
'dlc11_3':PostProc.DLC('dlc11_3'),
'dlc15_0':PostProc.DLC('dlc15_0'),
'dlc15_1':PostProc.DLC('dlc15_1'),
'dlc15_2':PostProc.DLC('dlc15_2')}


plt.rc('text', usetex=True)
for script in figScripts:
    module = importlib.import_module('Postprocessing.' + script)
    module.run(dlcs, SAVE = FigDir + script + '.png')
plt.rc('text', usetex=False)



