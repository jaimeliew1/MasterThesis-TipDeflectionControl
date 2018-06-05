# -*- coding: utf-8 -*-
"""
A module which performs analysis on a certain aspect of the tip deflection
controller results.

This script analyses: Vs Azimuth

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def lowerPeaks(X):
    peaks = []
    for i, x in enumerate(X):
        if i == 0 or i == len(X)-1:
            continue

        if (X[i-1] > x) and (X[i+1] > x):
            peaks.append(x)
    return peaks

def run(dlc, dlc_noipc, SAVE=None):
    dlc15_2 = PostProc.DLC('dlc15_2')

    wsp = 18
    c = 'ipc07'
    Sims = []
    Sims.append(dlc15_0(wsp=wsp)[0])
    Sims.append(dlc15_1(controller=c, wsp=wsp)[0])
    Sims.append(dlc15_2(controller=c, wsp=wsp, _amp=1)[0])
    Sims.append(dlc15_2(controller=c, wsp=wsp, _amp=2)[0])
    Sims.append(dlc15_2(controller=c, wsp=wsp, _amp=3)[0])
    labels = ['no control', 'TTT 0m', 'TTT 1m', 'TTT 2m', 'TTT 3m']

    channels = {'tcl':111}


    plt.figure()
    histProps = {'bins'     : 30,
             'range'    :[8, 25],
             'alpha'    : 0.7,
             'normed'   : True,
             'histtype' : 'stepfilled',
             'edgecolor': 'k'}
    # http://colorbrewer2.org/
    colors = ['tab:orange', '#ffffcc','#a1dab4','#41b6c4','#225ea8']
    plt.xlabel('Minimum Tower Clearance [m]')
    plt.ylabel('Probability [-]')
    for i, sims in enumerate(Sims):
        tcl = []
        for sim in sims:
            data = sim.loadFromSel(channels)
            tcl += lowerPeaks(data.tcl)

        if labels:
            label = labels[i]
        else:
            label = ''
        plt.hist(tcl, label=label, **histProps, fc=colors[i])

    plt.legend()
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()



if __name__ is '__main__':
    dlc15_0 = PostProc.DLC('dlc15_0')
    dlc15_1 = PostProc.DLC('dlc15_1')

    wsp = 18
    c = 'ipc07'
    run(dlc15_0, dlc15_1, SAVE=False)
