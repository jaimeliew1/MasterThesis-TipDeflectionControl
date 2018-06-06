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



def lowerPeaks(t, X):
    T, peaks = [], []
    for i, x in enumerate(X):
        if i == 0 or i == len(X)-1:
            continue

        if (X[i-1] >= x) and (X[i+1] > x):
            T.append(t[i])
            peaks.append(x)
    return np.array(T), np.array(peaks)





def run(dlcs, SAVE=None):
    wsp = 18
    seed = dlcs['dlc15_0'](wsp=wsp)[0][0]


    data = seed.loadFromSel(channels={'t':1, 'tcl':111})
    t = data.t
    tcl = data.tcl
    T, valleys = lowerPeaks(t, tcl)


    plt.figure(figsize=[8, 4])
    plt.xlabel('Time [s]')
    plt.ylabel('Minimum tower clearance [m]')
    start = 100#340
    plt.xlim(start, start + 100)
    plt.plot(t, tcl)
    plt.plot(T, valleys, 'xr')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()

    return T, valleys



if __name__ is '__main__':
    dlcs = {
    'dlc15_0':PostProc.DLC('dlc15_0')}

    T, valleys = run(dlcs, SAVE=False)
