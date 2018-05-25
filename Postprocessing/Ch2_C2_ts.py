# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc, dlc_noipc, SAVE=None):

    wsp=20
    channels = {'t'         : 1,
                'Azim'      : 2,
                'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}
    # get ref sim data
    seed = dlc_noipc(wsp=wsp)[0][0]
    data = seed.loadFromSel(channels)
    t = data.t
    td = -data[['TD1', 'TD2', 'TD3']].as_matrix()



    # get controlled sim data
    seed = dlc(wsp=wsp, controller='ipc07')[0][0]
    data = seed.loadFromSel(channels)
    td1 = -data[['TD1', 'TD2', 'TD3']].as_matrix()


    # subtract the mean
    td -= np.reshape(td.mean(1), [-1, 1])
    td1 -= np.reshape(td1.mean(1), [-1, 1])

    tstart = 300
    # Set up plot
    fig, ax = plt.subplots()
    ax.plot(t - tstart, td[:,0])
    ax.plot(t - tstart, td1[:,0])
    ax.set_xlim(0, 100)

    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Tip Deflection Purturbation [m]')
    ax.legend(['Without Control', 'With Control'], ncol=2)
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()




if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    run(dlc, dlc_noipc, SAVE=False)