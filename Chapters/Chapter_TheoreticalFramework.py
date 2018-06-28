# -*- coding: utf-8 -*-
"""
Make plots for Theoretical Framework Chapter.
@author: J
"""

import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
import importlib, os

OVERWRITE = False
FigDir = '../Figures/Chapter_TheoreticalFramework/'
if not os.path.isdir(FigDir):
    os.makedirs(FigDir)

existingFigs = [x[:-4] for x in os.listdir(FigDir)]
figScripts = [x[:-3] for x in os.listdir('../Postprocessing') if 'Ch1_' in x]

dlc_noipc = PostProc.DLC('dlc11_0')

plt.rc('text', usetex=True)
for script in figScripts:
    if any(script in x for x in existingFigs) and (not OVERWRITE):
        print(f'{script} figures already exists.')
    else:
        print(f'Running {script}.py...')
        module = importlib.import_module('Postprocessing.' + script)
        module.run(dlc_noipc, SAVE = FigDir + script + '.png')
plt.rc('text', usetex=False)



