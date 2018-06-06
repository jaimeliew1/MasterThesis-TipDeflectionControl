# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from Modelling import BladeModel
from JaimesThesisModule import ControlDesign
from Controllers import ControllerEvaluation
from Controllers import IPC04, IPC07



def plot_T(T1, T2, SAVE=False):
    # Calculate gain and phase response.
    f = np.linspace(0, 1.5, 1000)[1:]
    _, mag, phase = signal.bode(T1, w=f*(2*np.pi))
    _, mag2, phase2 = signal.bode(T2, w=f*(2*np.pi))
    phase = (phase + 180) % 360 - 180
    phase2 = (phase2 + 180) % 360 - 180


    fig, ax = ControllerEvaluation.bodeSetup(F1p=0.16)
    ax[0].plot(f, mag, label='$C_{f1p}$')
    ax[0].plot(f, mag2, label='$C_2$')
    ax[1].plot(f, phase)
    ax[1].plot(f, phase2)
    ax[0].legend(loc='lower left')

    ax[0].set_ylim([-10, 5])

    # plot x at f1p
    f1p = np.array([0.16])
    _, mag, phase = signal.bode(T1, w=f1p*(2*np.pi))
    ax[0].plot(f1p, mag, 'xr')
    ax[1].plot(f1p, phase, 'xr')

    _, mag2, phase2 = signal.bode(T2, w=f1p*(2*np.pi))
    ax[0].plot(f1p, mag2, 'xr')
    ax[1].plot(f1p, phase2, 'xr')


    with open('../Figures/Tables/Ch3_T.txt', 'w') as f:
        A = 1/10**(mag[0]/20)
        A2 = 1/10**(mag2[0]/20)
        banana = '{f1p}'
        f.write(f'$C_{banana}$ & {A:2.2f} & {phase[0]:2.2f} \\\\\n')
        f.write(f'$C_2$ & {A2:2.2f} & {phase2[0]:2.2f}')


    if SAVE:
        plt.savefig(SAVE, dpi=200)
    plt.show(); print()


def run(dlcs, SAVE=None):
    wsp =  18
    C1 = IPC04.make()
    C2 = IPC07.make()
    P = BladeModel.Blade(wsp)
    sys1 = ControlDesign.Turbine(P, C1)
    sys2 = ControlDesign.Turbine(P, C2)

    #ControllerEvaluation.plot_nyquist(sys.L, zoom=1.5, rightticks = True, save=SAVE)
    plot_T(sys1.T, sys2.T, SAVE=SAVE)


if __name__ == '__main__':
    run(0, 0)

