# -*- coding: utf-8 -*-
"""
Created on Fri May 18 09:48:24 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy import signal
from Modelling import BladeModel, OLResponse
from JaimesThesisModule import ControlDesign

from IPC07 import make

f = np.linspace(0, 1.5, 1000)[1:]

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



def plot_L(L, margins=False, save=False):
    # Calculate gain and phase response.
    _, mag, phase = signal.bode(L, w=f*2*np.pi)
    phase = (phase+180) % 360 - 180
    fig, ax = bodeSetup(F1p=0.16)

    ax[0].plot(f, mag, label='PC')
    ax[1].plot(f, phase)
    ax[0].legend()

    if margins:
        gm, pm = Margins(L)

        for freq, g in gm.items():
            ax[0].plot([freq]*2, [0, g], 'r', lw=0.5)
        for freq, p in pm.items():
            if p < 0:
                ax[1].plot([freq]*2, [-180, p], 'r', lw=0.5)
            if p >= 0:
                ax[1].plot([freq]*2, [180, p], 'r', lw=0.5)
    ## TODO, show gain and phase margins
    if save:
        plt.savefig('../Figures/{}/{}_L.png'.format(save, save), dpi=200)

    plt.show(); print()




def Margins(L, N=1000, fmax=1.5):
    # returns the gain margins (the gain [dB] when the phase crosses 180deg)
    # and the phase response [deg] when the gain crosses 0dB. Both in
    # dictionaries. Searches between f=0 to fmax Hz over N steps. Once a
    # crossover is found, a refined search is performed by dividing the
    # step into another N steps and finding the crossover. Therefore the
    # max error in the crossover frequencies is e > fmax/N**2 Hz
    f = np.linspace(0, fmax, N+1)[1:]
    _, mag, phase = signal.bode(L, w=f*2*np.pi)

    ##### Find phase margins ####

    # sweep find gain crossovers
    gainCross = []
    for i in range(N-1):
        if mag[i]*mag[i+1] < 0:
            # refine search
            f_ = np.linspace(f[i], f[i+1], N)
            _, mag_, _ = signal.bode(L, w=f_*2*np.pi)
            for j in range(N-1):
                if mag_[j]*mag_[j+1] < 0:
                    gainCross.append(f_[j])
                    break

    # calculate phase response at gain crossover frequencies
    pm = signal.bode(L, w=2*np.pi*np.array(gainCross))[2]
    pm = dict(zip(gainCross, pm))


    ###### Find Gain Margins #######
    # find phase crossover frequencies
    phaseCross = []
    for i in range(N-1):
        if (phase[i]+180)//360 != (phase[i+1]+180)//360:
            # refine search
            f_ = np.linspace(f[i], f[i+1], N)
            _, _, phase_ = signal.bode(L, w=f_*2*np.pi)
            for j in range(N-1):
                if (phase_[j]+180)//360 != (phase_[j+1]+180)//360:
                    phaseCross.append(f_[j])
                    break

    # calculate gain margin from phase crossover
    gm = signal.bode(L, w=2*np.pi*np.array(phaseCross))[1]
    gm = dict(zip(phaseCross, gm))

    return gm, pm



if __name__ is '__main__':

    wsp =  18

    # Load transfer functions
    C = make()
    P = BladeModel.Blade(wsp)
    Yol = OLResponse.Response(wsp)

    # Make close loop system object
    sys = ControlDesign.Turbine(P, C)

    # transfer function to find stability margins
    L = sys.L


    gm, pm = Margins(L)

    plot_L(L, margins=True)

