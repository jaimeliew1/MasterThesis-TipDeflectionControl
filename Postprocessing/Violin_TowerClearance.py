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
import seaborn as sns

def lowerPeaks(X):
    # Finds and lists the lower peaks (valleys) in a time series by finding
    # reversals. Only returns the values, not the index/time.
    peaks = []
    for i, x in enumerate(X):
        if i == 0 or i == len(X)-1:
            continue

        if (X[i-1] > x) and (X[i+1] > x):
            peaks.append(x)
    return peaks



def run(dlc1, dlc2, labels=['1','2'], SAVE=None):


    x, y, hue = np.array([]), np.array([]), np.array([])

    print('Analysing DLC1...')
    for sim in dlc1:
        for seed in sim:
            tcl = lowerPeaks(seed.Data.tcl)
            N = len(tcl)
            x = np.append(x, np.ones(N)*sim.wsp)
            y = np.append(y, tcl)
            hue = np.append(hue, [labels[0]]*N)
        print('wsp={} done.'.format(sim.wsp))

    print('Analysing DLC2...')
    for sim in dlc2:
        for seed in sim:
            tcl = lowerPeaks(seed.Data.tcl)
            N = len(tcl)
            x = np.append(x, np.ones(N)*sim.wsp)
            y = np.append(y, tcl)
            hue = np.append(hue, [labels[1]]*N)
        print('wsp={} done.'.format(sim.wsp))

    print('Making violin plot...')
    plt.figure()
    sns.set_style("whitegrid")
    plt.figure(figsize=[7,5])
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Minimum Tower Clearance [m]')
    sns.violinplot(x=x, y=y, hue=hue, split=True)
    plt.legend(loc='upper left')


    if SAVE:
        plt.savefig('../Figures/InverseShear/TowerClearance_inverse.png', dpi=200)

    plt.show(); print()
    return x, y, hue



if __name__ is '__main__':
    _locals = locals().keys()
    if not all(x in _locals for x in ['dlc15_0', 'dlc15_1', 'dlc11_0', 'dlc11_1']):
        dlc15_0 = PostProc.DLC('dlc15_0')
        dlc15_0.analysis(mode='fullload')

        dlc15_1 = PostProc.DLC('dlc15_1')
        dlc15_1.analysis(mode='fullload')

        dlc11_0 = PostProc.DLC('dlc11_0')
        dlc11_0.analysis(mode='fullload')

        dlc11_1 = PostProc.DLC('dlc11_1')
        dlc11_1.analysis(mode='fullload')



    x, y, hue = run(dlc15_0, dlc15_1(controller='ipc07'),
        labels=['no control', 'Tip Disturbance Rejection Control'], SAVE=True)

    print(min(y[hue=='no control']))
    print(min(y[hue=='Tip Disturbance Rejection Control']))

