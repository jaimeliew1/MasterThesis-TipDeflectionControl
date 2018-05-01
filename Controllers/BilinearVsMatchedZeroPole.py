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

from IPC05 import make

SAVE = False

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
    Fs = 5
    Cbi = discretise(C, Fs=Fs)
    Czp = discretise(C, Fs=Fs, method='matchedzeropole')


    # Calculate continuous frequency response
    wa, maga, phasea = signal.bode(C, n=1000)
    phasea = (phasea+180) % 360 - 180
    fa = wa/(2*np.pi)


    # plot
    fig, ax = bodeSetup(xlim=[0.01, 5], F1p=0.16)
    #ax[0].set_ylim([-100, 2])


    # calculate discrete frequency response

    wd, Hd = signal.freqz(Cbi.num, Cbi.den, worN=1024*8)
    fd = wd/np.pi*(Fs/2)
    magd, phased = 20*np.log10(abs(Hd)), np.angle(Hd, deg=True)
    phased = (phased + 180) % 360 - 180
    ax[0].plot(fd, magd, '-.')
    ax[1].plot(fd, phased, '-.', label = 'Bilinear')

    wd, Hd = signal.freqz(Czp.num, Czp.den, worN=1024*4)
    fd = wd/np.pi*(Fs/2)
    magd, phased = 20*np.log10(abs(Hd)), np.angle(Hd, deg=True)
    phased = (phased + 180) % 360 - 180
    ax[0].plot(fd, magd, '-.')
    ax[1].plot(fd, phased, '-.', label = 'Zero Pole Matching')


    ax[0].plot(fa, maga, 'k')
    ax[1].plot(fa, phasea, 'k', label='Continuous')
    ax[1].legend()
    if SAVE:
        plt.savefig('../Figures/discrete_bilinearVsZPM_fs={}.png'.format(Fs), dpi=200)





