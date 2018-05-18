# -*- coding: utf-8 -*-
"""
Analyses the correlation between root bending moment and tip deflection
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import Analysis, PostProc


def run(dlc_noipc, SAVE=None):
    #%% Load rbm and td data
    plt.rc('text', usetex=False)
    channels = {'t'         : 1,
                'RBM1'      : 26,
                'TD1'       : 49}

    wsp = 18
    seed = dlc_noipc(wsp=wsp)[0][0]
    data = seed.loadFromSel(channels=channels)
    t = list(data.t)
    X = list(data.RBM1)
    Y = list(-data.TD1)



    fig, ax1 = plt.subplots()
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Root Bending Moment [kNm]', color='b')
    ax1.tick_params('y', colors='b')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Tip Deflection [m]', color='r')
    ax2.tick_params('y', colors='r')

    ln1 = ax1.plot(t, X, lw=1, label='Flapwise Root Bending Moment')
    ln2 = ax2.plot(t, Y, '--r', lw=1, label = 'Flapwise Tip Deflection')
    ax1.set_xlim(100, 300)

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc='upper left')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.rc('text', usetex=True)



if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    plt.rc('text', usetex=True)
    run(dlc_noipc, SAVE=False)
    plt.rc('text', usetex=False)


