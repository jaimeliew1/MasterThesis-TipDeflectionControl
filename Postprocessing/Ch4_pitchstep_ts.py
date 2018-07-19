# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:52:45 2018

@author: J
TODO

"""

import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from JaimesThesisModule.Misc import readHawc2Res
from Configuration.Config import Config

#plt.rc('text', usetex=True)
save = False

def loadData():
    ''' loads time series data of pitch step simulations. from
    pitchstep_lin_xx.mat files, where xx is the wind speed [m/s].

    Return
    ^^^^^^
    WSP: List of wind speeds. These are the keys for the following dicts.
    T : Time [s] time series. Dictionary with wind speed as key.
    X : IPC Pitch demand [deg]. Dict
    Y : Tip deflection [m]. Dict
    '''
    dir_mat = '../Modelling/Data/'

    resFiles = [x for x in os.listdir(dir_mat) if x.endswith('.mat')]
    resFiles = [x for x in resFiles if x.startswith('pitchstep_lin')]

    WSP = [int(x.split('_')[2][:2]) for x in resFiles]

    X, Y, T = {}, {}, {}
    for wsp, fn in zip(WSP, resFiles):
        data = sio.loadmat(dir_mat + fn)
        T[wsp] = data['t'][0]
        X[wsp] = np.rad2deg(data['x'][0])
        Y[wsp] = data['y'][0]

    return WSP, T, X, Y

def run(SAVE=False):
    WSP, T, X, Y = loadData()

    #%% Plot
    wsp_ = [6, 12, 18, 24]
    fig, ax = plt.subplots(len(wsp_) + 1, 1, sharex=True, figsize=(6, 6))
    plt.subplots_adjust(hspace=0.1)
    ax[0].set_xlim(0, 75)
    ax[0].plot(T[4], X[4], 'tab:orange')
    for i, wsp in enumerate(wsp_):
        ax[i+1].plot(T[wsp], Y[wsp], label='Step response')
        ax[i+1].plot(T[wsp] + 40, Y[wsp]/2, ':k', label='Projected step response')
        ax[i+1].set_ylim(-1.4, 0.6)


# labels
    fig.text(0.06, 0.45, 'Tip Deflection [m]', va='center', rotation='vertical')
    fig.text(0.04, 0.8, 'IPC Pitch \n Demand [$^o$]', va='center', rotation='vertical')
    fig.text(0.5, 0.05, 'Time [s]', ha='center', rotation='horizontal')
    for i, wsp in enumerate(wsp_):
        ax[i+1].set_ylabel(f'$U={wsp}$ $m/s$')
        ax[i+1].yaxis.set_label_position('right')

    # over top legend
    ax[-1].legend(ncol=2,loc='lower right')
# manual adjustments
    ax[0].set_ylim(-0.1, 1.5)
    if SAVE:
        plt.savefig(SAVE[:-4]+'.png', dpi=200, bbox_inches='tight')
    plt.show(); print()


if __name__ is '__main__':
    run()