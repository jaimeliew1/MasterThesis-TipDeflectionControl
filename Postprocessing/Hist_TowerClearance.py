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

def run(*Sims, labels=None, SAVE=None):
    channels = {'tcl':111}
    plt.figure()
    plt.xlabel('Minimum Tower Clearance [m]')
    plt.ylabel('Frequency per 10 minute period')
    for i, sims in enumerate(Sims):
        tcl = []
        for sim in sims:
            data = sim.loadFromSel(channels)
            tcl += lowerPeaks(data.tcl)

        if labels:
            label = labels[i]
        else:
            label = ''
        plt.hist(tcl, 30, range=[5, 25], alpha=0.7, label=label)

    plt.legend()
    if SAVE:
        pass
        #plt.savefig('../Figures/InverseShear/TDvsAzim.png', dpi=200)

    plt.show(); print()



if __name__ is '__main__':
    dlc11_0 = PostProc.DLC('dlc11_0')
    dlc11_1 = PostProc.DLC('dlc11_1')
    dlc11_2 = PostProc.DLC('dlc11_2')
    dlc15_0 = PostProc.DLC('dlc15_0')
    dlc15_1 = PostProc.DLC('dlc15_1')



    #run(dlc15_0(wsp=12)[0], dlc15_1(controller='ipc07', wsp=12)[0],
    #    labels=['no control', 'TDR'], SAVE=False)

    run(dlc11_0(wsp=26)[0], dlc11_1(controller='ipc07', wsp=26)[0],
        labels=['no control', 'TDR'], SAVE=False)
    run(dlc11_0(wsp=26)[0], dlc11_2(controller='ipc_rbm07', wsp=26)[0],
        labels=['no control', 'RBM'], SAVE=False)