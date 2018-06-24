# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from JaimesThesisModule import PostProc
from scipy.stats import gaussian_kde



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




def kde_scipy(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    # Note that scipy weights its bandwidth by the covariance of the
    # input data.  To make the results comparable to the other methods,
    # we divide the bandwidth by the sample standard deviation here.
    #kde = gaussian_kde(x, bw_method=bandwidth / np.std(x, ddof=1), **kwargs)
    kde = gaussian_kde(x, bw_method=bandwidth, **kwargs)
    return kde.evaluate(x_grid)




def run(dlcs, SAVE=False):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_normal.png'
        SAVE2 = SAVE[:-4] + '_inverse.png'
    else:
        SAVE1 = SAVE2 = None
    _run(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'], SAVE=SAVE1)
    _run(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'], SAVE=SAVE2)




def _run(dlc_noipc, dlc, dlc2, wsp=18, c='ipc07', maxAmp=4, SAVE=False):

    # Load data for no IPC
    Sims = dlc_noipc(wsp=wsp)[0]
    X_noipc = []
    for seed in Sims:
        data = seed.loadFromSel(channels={'tcl': 111})
        X_noipc += list(data.tcl)

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


    cmap = mpl.cm.get_cmap('Blues')

    fig, ax = plt.subplots()

    x_ = np.linspace(9, 24, 100)
    for i, x in enumerate(X):
        label = f'$A_r={{{i}}}m$'
        c = cmap((i+1)/(len(X)))
        kde = kde_scipy(lowerPeaks(x), x_, bandwidth=0.15)
        plt.plot(x_, kde, color=c, label=label)


    kde = kde_scipy(lowerPeaks(X_noipc), x_, bandwidth=0.15)
    plt.plot(x_, kde, '--', color='tab:orange', label='no IPC')

    # labels
    ax.set_xlabel('Minimum Passing Blade-Tower Clearance [m]')
    ax.set_ylabel('Probability [-]')

    # ticks
    ax.set_xlim(9, 24)
    start, stop = ax.get_xlim()
    ax.set_xticks(range(int(start), int(stop)+1, 1), minor=True)
    ax.set_yticks(np.arange(0, 0.41, 0.1))
    ax.legend()


    if SAVE:
        plt.savefig(SAVE, dpi=300, bbox_inches='tight')
    plt.show(); print()





if __name__ is '__main__':
    dlcs = {
    'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}

    run(dlcs, SAVE=False)





