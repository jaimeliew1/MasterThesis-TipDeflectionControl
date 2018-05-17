# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc



def binCyclicalData(T, Y, width=1):

    X = np.arange(0, 360, width)
    dat = {k:[] for k in X}
    for t, y in zip(T, Y):
        Bin = 0
        if t%360 != 0:
            Bin =X[X<t%360][-1]
        dat[Bin].append(y)
    return dat



def TTTplot(ax, X, Y):

    hexbinConfig = {'gridsize':30,
                    'extent':[0, 360, -10, 10],
                    'linewidths':1,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':1300}
    ax.set_ylim(-10, 10)
    hist = binCyclicalData(X, Y)
    bins = list(hist.keys())
    Max = [np.max(v) for v in hist.values()]
    Min = [np.min(v) for v in hist.values()]

    Hexplot = ax.hexbin(X, Y, cmap='Blues', **hexbinConfig)
    ax.plot(bins, Max, '--k', lw=1)
    ax.plot(bins, Min, '--k', lw=1)
    ax.set_xticks(range(0, 361, 90))
    ax.set_yticks(range(-8, 9, 4))
    ax.grid()

    return Hexplot # for the color bar





def run(dlc, dlc2, wsp=18, c='ipc07', SAVE=False):

    #%% Load data into list of x and list of y.
    X, Y = [], []
    channels = {'Azim': 2, 'TD1': 49, 'TD2' : 52, 'TD3': 55}
    key = 'TD1'

    # Load data for no TTT
    Sims = dlc(wsp=wsp, controller=c)[0]
    X.append([]); Y.append([])
    for seed in Sims:
        data = seed.loadFromSel(channels)
        X[-1] += list(data.Azim)
        Y[-1] += list(data[key])

    # Load data for TTT where amp = 1, 2, 3
    for a in [1, 2, 3]:
        Sims = dlc2(wsp=wsp, controller=c, _amp=a)[0]
        X.append([]); Y.append([])
        for seed in Sims:
            data = seed.loadFromSel(channels)
            X[-1] += list(data.Azim)
            Y[-1] += list(data[key])


    #%% Plot the statistical data.
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(6, 7))
    plt.subplots_adjust(hspace=0.1)
    for i, ax in enumerate(axes):
        hexPlot = TTTplot(ax, X[i], Y[i])
        ax.text(0.4, 0.88, f'{i}m tracking', transform=ax.transAxes)

    # labels
    fig.text(0.04, 0.5, 'Flapwise Tip Deflection (blade FOR) [m]', va='center', rotation='vertical')
    axes[-1].set_xlabel('Azimuth Angle [deg]')
    # color bar
    N = len(X[0])
    cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist())
    cb.set_ticks(np.linspace(0, 1300, 6)) #based on vmin and vmax
    cb.set_ticklabels(['{:1.2f}%'.format(x*100) for x in np.linspace(0/N, 1300/N, 6)])
    cb.set_label('Probability of Occurences')

    axes[0].legend(['Min/Max'], loc='upper right')
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()







if __name__ is '__main__':
    dlc = PostProc.DLC('dlc11_1')
    dlc2 = PostProc.DLC('dlc11_3')

    plt.rc('text', usetex=True)
    run(dlc, dlc2, SAVE='../Figures/TTT_azim.png')
    plt.rc('text', usetex=False)



