# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:08:41 2018

@author: J

loads HAWC2 result data for tip deflection (without IPC) and
saves smoothed datapoints for the spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from JaimesThesisModule import PostProc



plt.rc('text', usetex=False)
SAVERESPONSE= False
PLOT = True
SAVEPLOT = False

Fs = 1/0.01


def freqResp(x, Fs, fmax=None):
    f  = np.linspace(0, Fs, len(x))
    Y = 2*abs(np.fft.fft(x))/len(x)

    if fmax:
        Y = Y[f <= fmax]
        f = f[f <= fmax]
    return f, Y

def plotSetup(wsp):
    fig, ax = plt.subplots()
    ax.set_ylabel('$|Y|$')
    ax.set_xlabel('Frequency [Hz]')
    fig.suptitle('Wsp: {}'.format(wsp))
    ax.set_xlim([0.01,5])
    ax.set_ylim([1e-4, 10])
    ax.set_yscale('log')
    ax.set_xscale('log')

    return fig, ax

def OLFreqResp(wsp, dlc_noipc, smooth= False):
    sim = dlc_noipc(yaw=0, wsp=wsp)[0]
    Ys = []
    for seed in sim:
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)

            if not smooth:
                f, Y = freqResp(seed.Data[key], Fs, fmax=10)
                Ys.append(Y)

            if smooth:
                f, Py = signal.welch(seed.Data[key], Fs, nperseg=1024*8)
                Ys.append(np.sqrt(Fs*Py/60000))

    Yave = np.mean(Ys, axis=0)


    return f, Yave


def saveResponse(f, Y, wsp):
    # saves the OL output data for a particular wind speed as a
    # csv with the filename OLResponse_{wsp}.csv
    filename = 'OLResponse_{}.csv'.format(wsp)
    np.savetxt('Data/'+ filename, np.vstack([f, Y]))





if __name__ is '__main__':
    # Load HAWC2 result data
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis(mode='fullload')

    WSP = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]

    for wsp in WSP:
        f, Y = OLFreqResp(wsp, dlc_noipc)
        f_, Y_ = OLFreqResp(wsp, dlc_noipc, smooth=True)

        if SAVERESPONSE:
            saveResponse(f_, Y_, wsp)


        if PLOT:
            fig, ax = plotSetup(wsp)
            ax.plot(f, Y)
            ax.plot(f_, Y_)

            ax.legend(['Mean Fourier Transform', 'Binned Mean Fourier Transform'], loc='lower left')

            if SAVEPLOT:
                plt.savefig('../Figures/OLResponse/OLResponse_{}.png'.format(wsp), dpi=200)
            plt.show(); print()


