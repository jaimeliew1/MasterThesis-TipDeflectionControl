# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
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


def cyclicalMinMax(X, Y):
    hist = binCyclicalData(X, Y)
    azim = list(hist.keys())
    Max = [np.max(v) for v in hist.values()]
    Min = [np.min(v) for v in hist.values()]

    return azim, Min, Max




def run(dlc, dlc_noipc, SAVE=None):

    wsp=20
    channels = {'Azim': 2,
                'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}
    # get ref sim data
    ref = dlc_noipc(wsp=wsp)[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim = data.Azim
            rbm = data[['RBM1', 'RBM2', 'RBM3']].as_matrix()
            td = -data[['TD1', 'TD2', 'TD3']].as_matrix()
        azim = np.append(azim, data.Azim)
        rbm = np.append(rbm, data[['RBM1', 'RBM2', 'RBM3']].as_matrix(), 0)
        td = np.append(td, -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)


    # get controlled sim data
    ref = dlc(wsp=wsp, controller='ipc07')[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim1 = data.Azim
            rbm1 = data[['RBM1', 'RBM2', 'RBM3']].as_matrix()
            td1 = -data[['TD1', 'TD2', 'TD3']].as_matrix()
        azim1 = np.append(azim1, data.Azim)
        rbm1 = np.append(rbm1, data[['RBM1', 'RBM2', 'RBM3']].as_matrix(), 0)
        td1 = np.append(td1, -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)
    td -= np.reshape(td.mean(1), [-1, 1])
    td1 -= np.reshape(td1.mean(1), [-1, 1])
    # Set up plot
    fig, ax = plt.subplots(3, 2, sharey=True, figsize=[7, 6])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)

    #extent = [0, 360, min(refy.min(), y.min()), max(refy.max(), y.max())]
    hexbinConfig = {'gridsize':30,
                    #'extent':extent,
                    'linewidths':0.25,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':1300}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25
    #ax[0,0].set_title('Root Bending moment')

    # labels
    fig.text(0.5, 0.02, 'Azimuth Angle [deg]', ha='center', rotation='horizontal')
    fig.text(0.01, 0.5, 'Tip Deflection [m]', va='center', rotation='vertical')


    for i in [0,1,2]:
        ax[i, 1].set_ylabel('Blade ' + str(i+1))
        ax[i, 1].yaxis.set_label_position("right")
        ax[i, 0].set_xticks([]); ax[i, 1].set_xticks([])
        #ax[i, 1].yaxis.tick_right()
        ax[i, 0].set_ylim(-6, 6)
        ax[i, 1].set_ylim(-6, 6)

    # Plotting
    for i in [0,1,2]: # for each blade
        ax[i, 0].hexbin(azim, td[:, i], cmap='Blues', **hexbinConfig)
        Azim_mm, Min, Max = cyclicalMinMax(azim, td[:, i])
        ax[i, 0].plot(Azim_mm, Min, '--k', lw=1)
        ax[i, 0].plot(Azim_mm, Max, '--k', lw=1)

        ax[i, 1].hexbin(azim1, td1[:,i], cmap='Blues',** hexbinConfig)
        Azim_mm, Min, Max = cyclicalMinMax(azim1, td1[:, i])
        ax[i, 1].plot(Azim_mm, Min, '--k', lw=1, label='Min/Max')
        ax[i, 1].plot(Azim_mm, Max, '--k', lw=1)

        ax[i,0].autoscale(axis='x')
        ax[i,1].autoscale(axis='x')

    # post set up
    ax[2,0].set_xticks([0, 120, 240, 360])
    ax[2,1].set_xticks([120, 240, 360])
    #ax[0,0].axvline(x=45, c='w', ls='--', lw=1)
    ax[0, 0].set_title('CPC')
    ax[0, 1].set_title('CPC and IPC')

    ax[2, 1].legend()
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()
    return td, rbm



if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    td, rbm = run(dlc, dlc_noipc, SAVE=False)