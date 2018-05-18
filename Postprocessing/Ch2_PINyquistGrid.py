# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:44:40 2018

@author: J
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from Modelling import BladeModel, OLResponse
from JaimesThesisModule import ControlDesign
from Controllers.IPC_PI import make

def nyquistSetup(ax, zoom=None):
    t_ = np.linspace(0, 2*np.pi, 100)
    circx, circy = np.sin(t_), np.cos(t_)
    ax.axis('equal')
    ax.plot(circx, circy, '--', lw=1, c='0.7')
    ax.plot([-1], [0], 'xr')
    ax.set_xticks([])
    ax.set_yticks([])

    if zoom:
        ax.set_xlim([-zoom - 0.25, zoom-0.25])
        ax.set_ylim([-zoom, zoom])





def plot_nyquist(L, axes=None, zoom=None, margin=False, save=False):

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


    if save:
        plt.savefig(save, dpi=200)

    return sm


def run(dlc=None, dlc_noipc=None, SAVE=None):
    wsp =  18
    # Load transfer functions
    C = make()
    P = BladeModel.Blade(wsp)

    Kps, Tis = np.meshgrid([0.01, 0.015, 0.02], [0.5, 1, 2])

    fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(7,7))
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    for i in range(3):
        for j in range(3):
            C = make(Kp=Kps[i, j], Ti=Tis[i, j])
            sys = ControlDesign.Turbine(P, C)
            plot_nyquist(sys.L, axes=axes[i, j], zoom=1, margin=True)
            perf = sys.performance(0.16)[0]
            axes[i, j].text(0, 0, '$f_{1p}$: ' + '{:2.2f}\%'.format(perf*100), transform=axes[i, j].transAxes, va='bottom')

    fig.text(0.1, 0.5, 'Real', va='center', rotation='vertical')
    fig.text(0.5, 0.1, 'Imaginary', ha='center', rotation='horizontal')

    for i in range(3):
        axes[0, i].set_title(f'$K_p=${Kps[0, i]}')
        axes[i,2].yaxis.set_label_position('right')
        axes[i, 2].set_ylabel(f'$T_i=${Tis[i, 0]}')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()

if __name__ == '__main__':

    run()




