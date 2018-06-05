# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc_noipc, dlc, dlc2, wsp=20, c='ipc04', SAVE=None):
    channels = {'Azim': 2,
                'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}
    # dictionary of time series keyed by TTT amplitude
    azim = {}
    td = {}
    # get ref sim data
    ref = dlc(wsp=wsp, controller=c)[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim[0] = data.Azim
            td[0] = -data[['TD1', 'TD2', 'TD3']].as_matrix()
        azim[0] = np.append(azim[0], data.Azim)
        td[0] = np.append(td[0], -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)


    # get controlled sim data
    refs = dlc2(wsp=wsp, controller='ipc07')
    for amp in [1, 2, 3]:
        ref = [x for x in refs if x.amp==amp][0]
        for i, seed in enumerate(ref):
            data = seed.loadFromSel(channels)
            if i == 0:
                azim[amp] = (data.Azim)
                td[amp] = (-data[['TD1', 'TD2', 'TD3']].as_matrix())
            azim[amp] = np.append(azim[amp], data.Azim)
            td[amp] = np.append(td[amp], -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)

    # Mean normalise
    for key in td.keys():
        td[key] -= np.reshape(td[key].mean(1), [-1, 1])


    fig, axes = plt.subplots(2, 2, sharey=True, sharex=True, figsize=[6, 6])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)


    hexbinConfig = {'gridsize':25,
                    #'extent':extent,
                    'linewidths':0.25,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':2000}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25

    # labels
    fig.text(0.4, 0.02, 'Azimuth Angle [deg]', ha='center', rotation='horizontal')
    fig.text(0.05, 0.5, 'Tip Deflection [m]', va='center', rotation='vertical')

    x = np.linspace(0, 360, 360)
    y = -np.cos(np.deg2rad(x))
    for i, key in enumerate(azim.keys()):
        ax = axes.ravel()[i]
        hexPlot = ax.hexbin(azim[key], td[key][:, 0], cmap='Blues', **hexbinConfig)
        if i == 0:
            ann = '$r(\phi) = 0$ [m]'
        else:
            ann = f'$r(\phi) = {key}\cos\phi$ [m]'
        ax.plot(x, key*y, '--r', lw=1.5, label=ann)
        ax.autoscale(axis='x')

        ax.legend(loc='lower center')



    # post set up
    ax.set_ylim(-6, 6)
    ax.set_xticks([90, 180, 270, 360])
    ax.set_yticks(np.arange(-5, 6, 2))

    N = len(azim[0])
    cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist())
    cb.set_ticks(np.linspace(0, 2000, 6)) #based on vmin and vmax
    ticklabels = ['{:1.1f}%'.format(x*100) for x in np.linspace(0/N, 2000/N, 6)]
    ticklabels[-1] = '$>$' + ticklabels[-1]
    cb.set_ticklabels(ticklabels)
    cb.set_label('Probability of Occurences')
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()




if __name__ is '__main__':

    dlc = PostProc.DLC('dlc15_1')
    dlc2 = PostProc.DLC('dlc15_2')

    run(None, dlc, dlc2, SAVE=False)