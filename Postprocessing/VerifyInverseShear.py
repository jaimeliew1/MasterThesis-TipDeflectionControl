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


def run(dlc1, dlc2, SAVE=None):

    wsp=16; keyroot='TD'; ylabel='Tip Deflection [m]'
    keys = [keyroot + str(x) for x in [1,2,3]]

    # get ref1 sim data
    ref1 = dlc1(yaw=0, wsp=wsp)[0]
    ref2 = dlc2(yaw=0, wsp=wsp)[0]

    for i, seed in enumerate(ref1):
        if i == 0:
            refx = seed.Data.Azim
            refy = seed.Data[keys].as_matrix()
        refx = np.append(refx, seed.Data.Azim)
        refy = np.append(refy, seed.Data[keys].as_matrix(), 0)

     # get ref2 sim data
    for i, seed in enumerate(ref2):
        if i == 0:
            ref2x = seed.Data.Azim
            ref2y = seed.Data[keys].as_matrix()
        ref2x = np.append(ref2x, seed.Data.Azim)
        ref2y = np.append(ref2y, seed.Data[keys].as_matrix(), 0)

    # Set up plot
    fig, ax = plt.subplots(3, 2, sharey=True, figsize=[7, 6])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)

    extent = [0, 360, min(refy.min(), ref2y.min()), max(refy.max(), ref2y.max())]
    hexbinConfig = {'gridsize':30, 'extent':extent, 'linewidths':1}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25
    ax[0,0].set_title('Normal Shear')
    ax[2,0].set_xlabel('Azimuth Angle [deg]')

    ax[0,1].set_title('Inverse Shear')
    ax[2,1].set_xlabel('Azimuth Angle [deg]')

    ax[1, 0].set_ylabel(ylabel)
    for i in [0,1,2]:
        ax[i, 1].set_ylabel('Blade ' + str(i+1))
        ax[i, 1].yaxis.set_label_position("right")
        ax[i, 0].set_xticks([]); ax[i, 1].set_xticks([])

    # Plotting
    for i in [0,1,2]: # for each blade
        ax[i, 0].hexbin(refx, refy[:, i], cmap='inferno', **hexbinConfig)
        ax[i, 1].hexbin(ref2x, ref2y[:,i], cmap='inferno',** hexbinConfig)
        ax[i,0].autoscale()
        ax[i,1].autoscale()

    # post set up
    ax[2,0].set_xticks([0, 120, 240, 360])
    ax[2,1].set_xticks([120, 240, 360])
    #ax[0,0].axvline(x=45, c='w', ls='--', lw=1)

    if SAVE:
        plt.savefig('../Figures/InverseShear/TDvsAzim.png', dpi=200)

    plt.show(); print()



if __name__ is '__main__':
    _locals = locals().keys()
    if not all(x in _locals for x in ['dlc15_0', 'dlc15_1', 'dlc11_0']):
        dlc15_0 = PostProc.DLC('dlc15_0')
        dlc15_0.analysis(mode='fullload')

        dlc15_1 = PostProc.DLC('dlc15_1')
        dlc15_1.analysis(mode='fullload')

        dlc11_0 = PostProc.DLC('dlc11_0')
        dlc11_0.analysis(mode='fullload')

    run(dlc11_0, dlc15_0, SAVE=True)