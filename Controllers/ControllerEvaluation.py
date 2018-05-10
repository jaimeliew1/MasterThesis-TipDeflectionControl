# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 08:54:42 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy import signal
from Modelling import BladeModel, OLResponse
from JaimesThesisModule import ControlDesign

#plt.rc('text', usetex=False)
F1p = [0.099, 0.1, 0.105, 0.14, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16]

from IPC_PI import make
#SAVE = 'ipc09'
SAVE=None


f = np.linspace(0, 1.5, 1000)



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


def magplotSetup(xlim = [0.01, 1.5], F1p=None):
    fig, axes = plt.subplots()
    axes.grid('off')
    axes.set_ylabel('Magnitude [dB]')
    axes.set_xlabel('Frequency [Hz]')
    axes.set_xlim(xlim)
    axes.set_xlim([0.01, xlim[1]])
    axes.set_xscale('log')

    # draw f_np lines
    if F1p is not None:
        for i in [1, 2, 3, 4]:
            axes.axvline(F1p*i, linestyle='--',color='k', lw=1)

    return fig, axes


def nyquistSetup(ax, zoom=None):
    t_ = np.linspace(0, 2*np.pi, 100)
    circx, circy = np.sin(t_), np.cos(t_)
    ax.axis('equal')
    ax.plot(circx, circy, '--', lw=1, c='0.7')
    ax.plot([-1], [0], 'xr')

    #ax.plot([-1, L(f_sm).real], [0, L(f_sm).imag], '--r', lw=0.5)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    if zoom:
        ax.set_xlim([-zoom, zoom])
        ax.set_ylim([-zoom, zoom])

################ Control Performance Plots
def plot_Pol_Pcl(P, P_CL, save=False):
    # Calculate gain and phase response.
    _, mag_P, phase_P = signal.bode(P, w=f*(2*np.pi))
    phase_P = (phase_P+180) % 360 - 180

    _, mag_CL, phase_CL = signal.bode(P_CL, w=f*(2*np.pi))
    phase_CL = (phase_CL+180) % 360 - 180

    fig, ax = bodeSetup(F1p=0.16)
    ax[0].plot(f, mag_P, label='Open Loop')
    ax[0].plot(f, mag_CL, label='Closed Loop')

    ax[1].plot(f, phase_P)
    ax[1].plot(f, phase_CL)

    ax[0].legend(loc='lower left')

    if save:
        plt.savefig('../Figures/{}/{}_OL_CL_bode.png'.format(save, save), dpi=200)



def plot_C(C, save=False):
    # Calculate gain and phase response.
    _, mag, _ = signal.bode(C, w=f*(2*np.pi))

    fig, ax = magplotSetup(F1p=0.16)
    ax.plot(f, mag, label='C')





    ax.legend()

    if save:
        plt.savefig('../Figures/{}/{}_C.png'.format(save, save), dpi=200)



def plot_S(S, save=False):
    # Calculate gain and phase response.
    _, mag, _ = signal.bode(S, w=f*(2*np.pi))

    fig, ax = magplotSetup(F1p=0.16)
    ax.plot(f, mag, label='Sensitivity function')


    # Draw area under curve
    verts = [(0, 0)] + list(zip(list(f), list(mag))) + [(f.max(), 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)


    ax.legend()

    if save:
        plt.savefig('../Figures/{}/{}_S.png'.format(save, save), dpi=200)



def plot_T(T, save=False):
    # Calculate gain and phase response.

    _, mag, phase = signal.bode(T, w=f*(2*np.pi))
    phase = (phase + 180) % 360 - 180


    fig, ax = bodeSetup(F1p=0.16)
    ax[0].plot(f, mag, label='Complementary Sensitivity function')

    ax[1].plot(f, phase)

    ax[0].legend(loc='lower left')


    # Draw area under curve
#    verts = [(0, 0)] + list(zip(list(f), list(mag))) + [(f.max(), 0)]
#    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
#    ax.add_patch(poly)

    if save:
        plt.savefig('../Figures/{}/{}_T.png'.format(save, save), dpi=200)



def plot_Yol_Ycl(Yol, S, save=False):

    w, H = signal.freqresp(S)
    f_ = w/(2*np.pi)

    fig, ax = magplotSetup(F1p=0.16)
    ax.set_ylabel('Magnitude [m]')
    ax.plot(f_, Yol(f_), '--k', label='$Y_{OL}$')
    ax.plot(f_, abs(H)*Yol(f_), label ='$Y_{CL}$ (predicted)')
    ax.set_xlim(f_.min(), 5)
    ax.legend()

    if save:
        plt.savefig('../Figures/{}/{}_Yol_Ycl.png'.format(save, save), dpi=200)



def plot_L(L, save=False):
    # Calculate gain and phase response.
    _, mag, phase = signal.bode(L, w=f*2*np.pi)
    phase = (phase+180) % 360 - 180


    fig, ax = bodeSetup(F1p=0.16)

    ax[0].plot(f, mag, label='PC')


    ax[1].plot(f, phase)
    ax[0].legend()

    ## TODO, show gain and phase margins
    if save:
        plt.savefig('../Figures/{}/{}_L.png'.format(save, save), dpi=200)




def plot_nyquist(L, zoom=1.5, save=False):
    fig, axes = plt.subplots(1, 2)
    plt.subplots_adjust(wspace=0.1)
    nyquistSetup(axes[0])
    nyquistSetup(axes[1], zoom=zoom)
    axes[1].yaxis.tick_right(); axes[1].set_ylabel('')


    w_ = np.linspace(0, 1.5, 1e4)*2*np.pi
    w_ = np.append(w_, [100])
    _, H = signal.freqresp(L, w=w_)
    axes[0].plot(H.real, H.imag, 'k', lw=1)
    axes[0].plot(H.real, -H.imag, '--k', lw=1)

    axes[1].plot(H.real, H.imag, 'k', lw=1)
    axes[1].plot(H.real, -H.imag, '--k', lw=1)

    # plot stability margin
    H_ = ControlDesign._stabilityMargin(w_, H)
    axes[1].plot([-1, H_.real], [0, H_.imag], '--r', lw=0.5)

    if save:
        plt.savefig('../Figures/{}/{}_nyquist.png'.format(save, save), dpi=200)








if __name__ == '__main__':

    wsp =  18

    # Load transfer functions
    C = make()
    P = BladeModel.Blade(wsp)
    Yol = OLResponse.Response(wsp)

    # Make close loop system object
    sys = ControlDesign.Turbine(P, C)
    L = sys.L
    S = sys.S
    T = sys.T
    P_CL = sys.CL


    # PLot Controller Performance
    plot_C(C, save=SAVE)
    plot_Pol_Pcl(P, P_CL, save=SAVE)
    plot_S(S, save=SAVE)
    plot_T(T, save=SAVE)
    plot_Yol_Ycl(Yol, S, save=SAVE)

    # Plot Controller Robust Stability
    plot_L(L, save=SAVE)
    plot_nyquist(L, zoom=1.5, save=SAVE)

    # determine tip trajectory tracking precompensator paramams
    _, mag, phase = signal.bode(T, w=0.16*2*np.pi)
    print('To achieve tip trajectory of A*cos(omega*t)')
    print('use {:2.2f}*A*cos(omega*t + {:2.2f}/180*pi)'.format(
            1/10**(mag[0]/20), phase[0]))


