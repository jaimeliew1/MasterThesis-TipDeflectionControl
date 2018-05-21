# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""

from Modelling import BladeModel
from JaimesThesisModule import ControlDesign
from Controllers.IPC07 import make
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal



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





def plot_nyquist(L, zoom=None, margin=False, rightticks = False, save=False):
    fig, axes = plt.subplots(figsize=[6,6])
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

    if rightticks:
        axes.yaxis.tick_right()
    if save:
        plt.savefig(save, dpi=200, bbox_inches='tight')
    plt.show(); print()
    return sm





def run(dlc=None, dlc_noipc=None, SAVE=None):
    wsp =  18
    C = make()
    P = BladeModel.Blade(wsp)
    sys = ControlDesign.Turbine(P, C)

    plot_nyquist(sys.L, zoom=1.5, rightticks = True, save=SAVE)
    #ControllerEvaluation.plot_L(sys.L, margins=True, save=SAVE)


if __name__ == '__main__':
    run()

