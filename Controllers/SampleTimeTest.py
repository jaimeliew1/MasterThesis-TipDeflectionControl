# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:16:19 2018

@author: J
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:21:39 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from Controllers.Discretisation import discretise

from IPC04 import make

SAVE = True

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







if __name__ == '__main__':
    C = make()
    Cd = []
    Fs = [1, 5, 20, 40, 100]
    for fs in Fs:
        Cd.append(discretise(C, Fs=fs))


    # Calculate continuous frequency response
    wa, maga, phasea = signal.bode(C, n=1000)
    phasea = (phasea+180) % 360 - 180
    fa = wa/(2*np.pi)


    # plot
    fig, ax = bodeSetup(xlim=[0.01, 100], F1p=0.16)
    ax[0].set_ylim([-100, 2])


    # calculate discrete frequency response
    for i, fs in enumerate(Fs):
        wd, Hd = signal.freqz(Cd[i].num, Cd[i].den, worN=1024*4)
        fd = wd/np.pi*(fs/2)
        magd, phased = 20*np.log10(abs(Hd)), np.angle(Hd, deg=True)
        ax[0].plot(fd, magd, '-.')
        ax[1].plot(fd, phased, '-.', label = '$f_s$={} Hz'.format(fs))


    ax[0].plot(fa, maga, 'k')
    ax[1].plot(fa, phasea, 'k', label='Continuous')
    ax[1].legend()
    if SAVE:
        plt.savefig('../Figures/discrete_sampletime.png', dpi=200)





