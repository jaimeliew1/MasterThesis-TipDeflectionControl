# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:43:36 2018

@author: J
"""
import numpy as np
from numpy import pi, sin, sqrt, log10
import matplotlib.pyplot as plt
from scipy import signal




def bode(system, fig=None ,axes=None):
    # calculate bode plot for system
    w, mag, phase = signal.bode(system, w=np.logspace(-1, 2.5, 1000))

    f = w/(2*pi)

    # set up plot
    if axes is None:
        fig, axes = plt.subplots(2, 1, figsize=[4,4], sharex=True)
        plt.subplots_adjust(hspace=0.05)
        axes[0].grid('off')
        axes[1].grid('off')
        axes[0].set_ylabel('Magnitude [dB]')
        axes[1].set_ylabel('Phase')
        axes[1].set_xlabel('Frequency')
        axes[0].set_xscale('log')
        axes[0].axhline(0, linestyle='-',color='0.7', lw=1)
        axes[1].axhline(0, linestyle='-',color='0.7', lw=1)

    # plot
    axes[0].plot(f, mag)
    axes[1].plot(f, phase)
    axes[0].autoscale(axis='x',tight=True)
    return fig, axes






def LeadCompensator(lead, freq, deg=False):
    '''
    Returns the transfer function of a lead compensator with a maximum
    lead angle at a particular frequency.

    Parameters
    ^^^^^^^^^^
    lead: Maximum phase lead [deg]
    freq: Frequency which the maximum phase lead occurs [rad/s]
    deg: if True, freq is in the units of Hz. Else, rad/s

    Return
    ^^^^^^
    signal.TransferFunction object.
    '''
    if deg:
        freq = freq * 2 *np.pi

    lead = lead * pi/180


    a = (1 + sin(lead))/(1 - sin(lead))
    T = 1/(sqrt(a) * freq)
    num = [a*T, 1]
    den = [T, 1]

    return signal.TransferFunction(num, den)




def LowpassFilter(freq, damp, deg=False):
    '''
    Returns the transfer function of a second order low
    pass filter defined with frequency and damping.

    Parameters
    ^^^^^^^^^^
    freq: Frequency which the maximum phase lead occurs [rad/s]
    damp: damping ratio [?]
    deg: if True, freq is in the units of Hz. Else, rad/s

    Return
    ^^^^^^
    signal.TransferFunction object.
    '''
    if deg:
        freq = freq*2*pi


    num = [freq**2]
    den = [1, 2*damp*freq, freq**2]

    return signal.TransferFunction(num, den)




def BandpassFilter(freqs, damps, deg=False):
    '''
    Returns the transfer function of a second order band
    pass filter defined with 2 frequences and 2 damping ratios.

    Parameters
    ^^^^^^^^^^
    freq: Frequency which the maximum phase lead occurs [rad/s]
    damp: damping ratio [?]
    deg: if True, freq is in the units of Hz. Else, rad/s

    Return
    ^^^^^^
    signal.TransferFunction object.
    '''
    if deg:
        freqs = [f*2*pi for f in freqs]


    num = [1, 2*damps[0]*freqs[0], freqs[0]**2]
    den = [1, 2*damps[1]*freqs[1], freqs[1]**2]

    return signal.TransferFunction(num, den)




def plot_leadcomp():
    lead, freq = 20, 1
    G = LeadCompensator(lead, freq, deg=True)
    fig, ax = bode(G)
    a  = (1 + sin(lead/180*pi))/(1 - sin(lead/180*pi))
    M_w = 20*log10(sqrt(a))
    # Plot 1 axis
    ax[0].axhline(M_w, lw=1, ls='--', c='k')
    ax[0].axvline(freq, lw=1, ls='--', c='k')
    ax[0].set_yticks([0, M_w])
    ax[0].set_yticklabels([0, '$M_w$'])
    ax[0].yaxis.tick_right()
    # Plot 2 axis
    ax[1].axhline(lead, lw=1, ls='--', c='k')
    ax[1].set_xticks([freq])
    ax[1].set_xticklabels(['$\omega$'])
    ax[1].set_yticks([0, lead])
    ax[1].set_yticklabels([0, '$\psi_{\omega}$'])
    ax[1].set_ylim([0, lead + 5])
    ax[1].axvline(freq, lw=1, ls='--', c='k')
    ax[1].yaxis.tick_right()


    return fig, ax



def plot_lowpass():
    f, z = 1, 0.1
    G = LowpassFilter(f, z, deg=True)
    fig, ax = bode(G)
    ax[0].axvline(f, lw=1, ls='--', c='k')
    ax[1].axhline(-90, lw=1, ls='--', c='k')
    ax[1].axvline(f, lw=1, ls='--', c='k')
    ax[0].axhline(20*log10(1/(2*z)), lw=1, ls='--', c='k')
    ax[1].set_xticks([f])
    ax[1].set_xticklabels(['$\omega_{cf}$'])
    ax[0].set_yticks([0, 20*log10(1/(2*z))])
    ax[0].set_yticklabels([0, '$M_{cf}$'])
    ax[0].set_ylim([-20, 20])
    ax[0].yaxis.tick_right()
    ax[1].set_yticks([0, -90])
    ax[1].set_yticklabels([0, '$-90^o$'])
    ax[1].yaxis.tick_right()

    return fig, ax




def plot_bandpass():
    f, z = [0.8, 2], [0.1, 0.3]
    G = BandpassFilter(f, z, deg=True)
    fig, ax = bode(G)
    ax[0].axvline(f[0], lw=1, ls='--', c='k')
    ax[0].axvline(f[1], lw=1, ls='--', c='k')
    ax[1].axvline(f[0], lw=1, ls='--', c='k')
    ax[1].axvline(f[1], lw=1, ls='--', c='k')

    ax[1].set_xticks(f)
    ax[1].set_xticklabels(['$\omega_{1}$', '$\omega_{2}$'])
#
#    ax[0].set_yticklabels(['$M_{max}$'], rotation=-90)
#    ax[0].set_ylim([-20, 20])
    ax[0].set_yticks([0])
    ax[0].yaxis.tick_right()
    ax[1].set_yticks([0])
    ax[1].yaxis.tick_right()

    return fig, ax



if __name__ == '__main__':
    plotfuncs = [plot_leadcomp, plot_lowpass, plot_bandpass]
    fn = ['Ch1_leadcomp', 'Ch1_lowpass', 'ch1_bandpass']


    plt.rc('text', usetex=True)
    for func, fn in zip(plotfuncs, fn):
        func()
        plt.savefig(f'../Figures/Chapter_TheoreticalFramework/{fn}.png', dpi=200)
        plt.show(); print()

    plt.rc('text', usetex=False)






