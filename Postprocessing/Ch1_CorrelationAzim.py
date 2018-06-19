# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc_noipc, SAVE=None):

    wsp=16
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

    # Set up plot
    fig, ax = plt.subplots(3, 2, figsize=[7, 5])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)

    #extent = [0, 360, min(refy.min(), y.min()), max(refy.max(), y.max())]
    hexbinConfig = {'gridsize':30,
                    #'extent':extent,
                    'linewidths':1,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':1300}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25
    #ax[0,0].set_title('Root Bending moment')

    # labels
    fig.text(0.5, 0.02, 'Azimuth Angle [deg]', ha='center', rotation='horizontal')
    fig.text(0.01, 0.5, 'Root Bending Moment [kNm]', va='center', rotation='vertical')
    fig.text(0.95, 0.5, 'Tip Deflection [m]', va='center', rotation='vertical')

    for i in [0,1,2]:
        #ax[i, 1].set_ylabel('Blade ' + str(i+1))
        #ax[i, 1].yaxis.set_label_position("right")
        string = f'Blade {i+1} RBM'
        ax[i, 0].text(0.5, 0.97, string, transform=ax[i, 0].transAxes, color='k', ha='center', va = 'top')

        string = f'Blade {i+1} Tip deflection'
        ax[i, 1].text(0.5, 0.97, string, transform=ax[i, 1].transAxes, color='k', ha='center', va = 'top')
        ax[i, 0].set_xticks([]); ax[i, 1].set_xticks([])
        ax[i, 1].yaxis.tick_right()

    # Plotting
    for i in [0,1,2]: # for each blade
        hexPlot = ax[i, 0].hexbin(azim, rbm[:, i], cmap='Blues', **hexbinConfig)
        ax[i, 1].hexbin(azim, td[:,i], cmap='Blues',** hexbinConfig)
        ax[i,0].autoscale()
        ax[i,1].autoscale()

    # post set up
    ax[2,0].set_xticks([0, 120, 240, 360])
    ax[2,1].set_xticks([120, 240, 360])
    #color bar
    N = len(azim)
    print('N:', N)
    cb = fig.colorbar(hexPlot, ax=ax.ravel().tolist(), location='top')
    cb.set_ticks(np.linspace(0, 1300, 6)) #based on vmin and vmax
    ticklabels = ['{:1.1f}\\%'.format(x*100) for x in np.linspace(0/N, 1300/N, 6)]
    ticklabels[-1] = '$>$' + ticklabels[-1]
    cb.set_ticklabels(ticklabels)
    cb.set_label('Probability of Occurences')


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()
    return td, rbm



if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    td, rbm = run(dlc_noipc, SAVE=False)