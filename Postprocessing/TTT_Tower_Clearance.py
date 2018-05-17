# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from JaimesThesisModule import PostProc



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





def run(dlc, dlc2, wsp=18, c='ipc04', maxAmp=3, SAVE=False):
    #%% Load data into list of x
    X = []

    # Load data for no TTT
    Sims = dlc(wsp=wsp, controller=c)[0]
    X.append([])
    for seed in Sims:
        data = seed.loadFromSel(channels={'tcl': 111})
        X[-1] += list(data.tcl)


    # Load data for TTT where amp = 1, 2, 3
    for a in range(1, maxAmp+1):
        Sims = dlc2(wsp=wsp, controller=c, _amp=a)[0]
        X.append([])
        for seed in Sims:
            data = seed.loadFromSel(channels={'tcl': 111})
            X[-1] += list(data.tcl)


    #%% Plot histogram of closest tower passes.
    histProps = {'bins'     : 30,
                 'alpha'    : 0.7,
                 'normed'   : True,
                 'histtype' : 'stepfilled',
                 'edgecolor': 'k'}

    cmap = mpl.cm.get_cmap('Blues')

    fig, ax = plt.subplots()
    for i, x in enumerate(X):
        label = f'{i}m tracking'
        c = cmap(i/(len(X)-1))
        ax.hist(lowerPeaks(x), **histProps, facecolor=c, label=label)
    # labels
    ax.set_xlabel('Minimum Passing Blade-Tower Clearance [m]')
    ax.set_ylabel('Probability [-]')

    # ticks
    start, stop = ax.get_xlim()
    ax.set_xticks(range(int(start), int(stop)+1, 1), minor=True)
    ax.set_yticks(np.arange(0, 0.41, 0.1))
    ax.legend()


    if SAVE:
        pass
        #plt.savefig('../Figures/{}/.png', dpi=200)
    plt.show(); print()





if __name__ is '__main__':
    dlc = PostProc.DLC('dlc11_1')
    dlc2 = PostProc.DLC('dlc11_3')


    run(dlc, dlc2, wsp=18, c='ipc04', maxAmp=4, SAVE=False)



#%%






