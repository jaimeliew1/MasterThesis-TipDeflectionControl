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
    _, mag, phase = signal.bode(L, w=f*2*np.pi)




    # sweep find gain crossovers
    N = len(f)
    gainCross = []
    for i in range(N-1):
        if mag[i]*mag[i+1] < 0:
            # refine search
            fsmall = np.linspace(f[i], f[i+1], 100)
            _, magsmall, _ = signal.bode(L, w=fsmall*2*np.pi)
            for j in range(99):
                if magsmall[j]*magsmall[j+1] < 0:
                    gainCross.append(fsmall[j])
                    break

    # find phase crossover frequencies
    phaseCross = []
    for i in range(N-1):
        if (phase[i]+180)//360 != (phase[i+1]+180)//360:
            # refine search
            fsmall = np.linspace(f[i], f[i+1], 100)
            _, _, phase_ = signal.bode(L, w=fsmall*2*np.pi)
            for j in range(99):
                if (phase_[j]+180)//360 != (phase_[j+1]+180)//360:
                    phaseCross.append(fsmall[j])
                    break

    # calculate phase margin from gain crossover
    pm = signal.bode(L, w=2*np.pi*np.array(gainCross))[2]
    pm = dict(zip(gainCross, pm))

    # calculate gain margin from phase crossover
    gm = signal.bode(L, w=2*np.pi*np.array(phaseCross))[1]
    gm = dict(zip(phaseCross, gm))

    print(pm, gm)
    phase = ((phase+180)%360 -180)
    #fig, ax = bodeSetup(F1p=0.16, xlim=[0.1246, 0.12612])
    #ax[0].set_ylim(-1, 1)
    fig, ax = bodeSetup(F1p=0.16)
    ax[0].plot(f, mag, label='PC')
    #ax[0].plot(gainCross, [0]*len(gainCross), 'xr')
    for freq, g in gm.items():
        ax[0].plot([freq]*2, [g, 0], 'r', lw=0.5)

    ax[1].plot(f, phase)
    #ax[1].plot(phaseCross, [180]*len(phaseCross), 'xr')
    for freq, ph in pm.items():
        if ph > 0:
            ax[1].plot([freq]*2, [ph, 180], 'r', lw=0.5)
        else:
            ax[1].plot([freq]*2, [-180, ph], 'r', lw=0.5)
    ax[0].legend()

