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

from IPC07 import make
#SAVE = 'ipc09'
SAVE=None


f = np.linspace(0, 1.5, 1000)[1:]

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
    pm = (pm + 180)%360 - 180
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


    axes[1].set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes[1].set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes[0].set_xticklabels([], minor=True)
    axes[1].grid(which='minor')
    axes[0].grid(which='minor')

    axes[0].axhline(0, linestyle='-',color='0.7', lw=1)
    return fig, axes


def magplotSetup(xlim = [0.01, 1.5], F1p=None):
    fig, axes = plt.subplots()
    axes.grid('off')
    axes.set_ylabel('Magnitude [dB]')
    axes.set_xlabel('Frequency [Hz]')
    axes.set_xlim(xlim)
    axes.set_xlim([0.01, xlim[1]])
    axes.set_xscale('log')

    axes.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes.set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes.grid(which='minor')

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
        plt.savefig(save, dpi=200)
    plt.show(); print()


def plot_C(C, save=False):
    # Calculate gain and phase response.
    _, mag, _ = signal.bode(C, w=f*(2*np.pi))

    fig, ax = magplotSetup(F1p=0.16)
    ax.plot(f, mag, label='C')


    ax.legend()

    if save:
        plt.savefig(save, dpi=200)
    plt.show(); print()


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
        plt.savefig(save, dpi=200)
    plt.show(); print()


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
        plt.savefig(save, dpi=200)
    plt.show(); print()


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
        plt.savefig(save, dpi=200)
    plt.show(); print()


def plot_L(L, margins=False, save=False):
    # Calculate gain and phase response.
    _, mag, phase = signal.bode(L, w=f*2*np.pi)
    phase = (phase+180) % 360 - 180
    fig, ax = bodeSetup(F1p=0.16)

    ax[0].plot(f, mag)
    ax[1].plot(f, phase, label='Loop Transfer Function')


    if margins:
        gm, pm = Margins(L)

        for freq, g in gm.items():
            ax[0].plot([freq]*2, [0, g], '--r', lw=1)
            ax[0].text(freq, g, '${:2.2f}dB$'.format(abs(g)), rotation=-90, fontsize=10, va='bottom')


        for freq, p in pm.items():
            if p < 0:
                ax[1].plot([freq]*2, [-180, p], '--r', lw=1)
                ax[1].text(freq, p-10, '${:2.0f}^o$'.format(p+180), rotation=-90, fontsize=10, va='top')
            if p >= 0:
                ax[1].plot([freq]*2, [180, p], '--r', lw=1)
                ax[1].text(freq, p+10, '${:2.0f}^o$'.format(180-p), rotation=-90, fontsize=10, va='bottom')


    ax[1].legend(['Loop Transfer Function', 'Gain/Phase Margins'])

    if save:
        plt.savefig(save, dpi=200, bbox_inches='tight')

    plt.show(); print()
    return ax

def plot_nyquist(L, zoom=None, margin=False, save=False):
    fig, axes = plt.subplots(figsize=[5, 5])

    nyquistSetup(axes, zoom=zoom)
    #axes[1].yaxis.tick_right(); axes[1].set_ylabel('')


    w_ = np.linspace(0, 1.5, 10**4)*2*np.pi
    w_ = np.append(w_[1:], [100])
    _, H = signal.freqresp(L, w=w_)

    axes.plot(H.real, H.imag, 'k', lw=1, label='Nyquist Plot')
    axes.plot(H.real, -H.imag, '--k', lw=1)

    # plot stability margin
    sm, H_ = ControlDesign._stabilityMargin(w_, H)
    axes.plot([-1, H_.real], [0, H_.imag], '--r', lw=1, label='Stability Margin, $s_m$')

    angle = np.rad2deg(np.arctan(H_.imag/(H_.real + 1)))
    axes.text(-0.5 + H_.real/2, H_.imag/2, '${:2.2f}$'.format(sm), rotation=angle, ha='center', va='bottom')
    axes.legend(loc='lower left')

    if save:
        plt.savefig(save, dpi=200)
    plt.show(); print()
    return sm





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

    ax = plot_L(L, margins=True, save=SAVE)
    sm = plot_nyquist(L, zoom=1.5, save=SAVE)

    # determine tip trajectory tracking precompensator paramams
    _, mag, phase = signal.bode(T, w=0.16*2*np.pi)
    print('To achieve tip trajectory of A*cos(omega*t)')
    print('use {:2.2f}*A*cos(omega*t + {:2.2f}/180*pi)'.format(
            1/10**(mag[0]/20), phase[0]))
    print('Stability Margin: sm = {:2.3}'.format(sm))
    for i in [1, 2, 3, 4]:
        _, H = signal.freqresp(S, w=i*0.16*2*np.pi)
        print('f_{}p performance: {:2.2f}%'.format(i, abs(H[0])*100-100))



