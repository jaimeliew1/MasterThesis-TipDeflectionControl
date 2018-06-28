# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:21:39 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from JaimesThesisModule.ControlDesign import MatchedZeroPole, saveHTC

from Controllers.IPC_PI import make
Fs = 100
SAVE = True
filename = 'ipc_pi.htc'


def bodeSetup(xlim = [0.01, 1.5], F1p=None):
    fig, axes = plt.subplots(2, 1, figsize=[6,6], sharex=True)
    plt.subplots_adjust(hspace=0.05)
    axes[0].grid('off')
    axes[1].grid('off')
    axes[0].set_ylabel('Magnitude [dB]')
    axes[1].set_ylabel('Phase [deg]')
    axes[1].set_xlabel('Frequency [Hz]')

    axes[1].set_ylim([-180, 180])
    axes[0].set_xlim(xlim)
    axes[1].set_yticks(np.arange(-180, 180, 60))
    axes[0].set_xscale('log')

    # draw f_np lines
    if F1p is not None:
        for i in [1, 2, 3, 4]:
            axes[0].axvline(F1p*i, linestyle='--',color='k', lw=1)
            axes[1].axvline(F1p*i, linestyle='--',color='k', lw=1)

    axes[0].axhline(0, linestyle='--',color='0.7', lw=1)
    return fig, axes





def discretise(C, Fs=100, method='bilinear', save=None):
    # discretizes the controller transfer function and saves it to file.
    if method == 'bilinear':
        coefz = signal.bilinear(C.num, C.den, fs=Fs)
    elif method.lower() == 'matchedzeropole':
        coefz = MatchedZeroPole(C.num, C.den, 1/Fs)

    Cd = signal.TransferFunction(coefz[0], coefz[1], dt = 1/Fs)

    return Cd


if __name__ == '__main__':
    C = make()
    Cd = discretise(C, Fs=Fs)


    saveHTC(Cd.num, Cd.den, filename)


    # Calculate continuous  frequency response
    wa, maga, phasea = signal.bode(C, n=1000)
    phasea = (phasea+180) % 360 - 180
    fa = wa/(2*np.pi)

    # calculate discrete frequency response
    wd, Hd = signal.freqz(Cd.num, Cd.den, worN=1024*4)
    fd = wd/np.pi*(Fs/2)
    magd, phased = 20*np.log10(abs(Hd)), np.angle(Hd, deg=True)

    # plot
    fig, ax = bodeSetup(xlim=[0.01, 10], F1p=0.16)
    ax[0].set_ylim([-100, 2])
    ax[0].plot(fa, maga, 'k', label='$C$ (Continuous)')
    ax[1].plot(fa, phasea, 'k')

    ax[0].plot(fd, magd, '-.r', label = '$C$ (Discrete)')
    ax[1].plot(fd, phased, '-.r')

    ax[0].legend()
    if SAVE:
        plt.savefig('../Figures/Ca_Cd.png', dpi=200)




