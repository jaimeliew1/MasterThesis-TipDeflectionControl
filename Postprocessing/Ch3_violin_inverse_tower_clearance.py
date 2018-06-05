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



def formatViolinplot(parts, colors=None):

    for i, pc in enumerate(parts['bodies']):
        if colors:
            pc.set_facecolor(colors[i])
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    for key in ['cbars', 'cmins', 'cmaxes', 'cmeans']:
        parts[key].set_color('black')
        parts[key].set_linewidth(1)




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
    labels = ['no\nIPC', 'TTT 0m', 'TTT 1m', 'TTT 2m', 'TTT 3m']
    keys = ['nocontrol', 0, 1, 2, 3]
    channels = {'tcl':111}




    X = {}
    for i, sims in enumerate(Sims):
        tcl = []
        for sim in sims:
            data = sim.loadFromSel(channels)
            tcl += lowerPeaks(data.tcl)

        X[keys[i]] = tcl

    plt.figure(figsize=[4, 4])
    #plt.xlim(-12, 12)

    plt.xlabel('Minimum Tower Clearance $[m]$')
    plt.ylabel('Tip Tracking Amplitude $[m]$')
    parts = plt.violinplot(X.values(), positions=np.arange(len(X)), vert=False, showmeans=True)
    # http://colorbrewer2.org/
    colors = ['0.7', '#ffffcc','#a1dab4','#41b6c4','#225ea8']
    formatViolinplot(parts, colors)
    plt.yticks(np.arange(len(X)), labels)



    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()



if __name__ is '__main__':
    dlc15_0 = PostProc.DLC('dlc15_0')
    dlc15_1 = PostProc.DLC('dlc15_1')


    run(dlc15_0, dlc15_1, SAVE=False)
