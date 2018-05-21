# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""

from Controllers import ControllerEvaluation
from Modelling import BladeModel
from JaimesThesisModule import ControlDesign
import importlib
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def run(dlc=None, dlc_noipc=None, SAVE=None):
    f = np.linspace(0, 1.5, 1000)[1:]
    C = []
    modules = ['IPC_PI', 'IPC04', 'IPC09', 'IPC10', 'IPC11']
    for m in modules:
        module = importlib.import_module('Controllers.' + m)
        C.append(module.make)


    Mag = []
    for i in [0, 1, 2, 3, 4]:
        P = BladeModel.Blade(18)
        sys = ControlDesign.Turbine(P, C[i]())
        Mag.append(signal.bode(sys.S, w=f*(2*np.pi))[1])

    fig, ax = ControllerEvaluation.magplotSetup(F1p=0.16)
    ax.set_xlim(0.05, 1.5)

    ax.plot(f, Mag[0], label='$S(C_{PI})$')
    for i in [1, 2, 3, 4]:
        ax.plot(f, Mag[i], '-.', label='$S(C_{f' + f'{i}' + 'p})$')



    ax.set_ylim(-25, 10)

    ax.legend()

    if SAVE:
        plt.savefig(SAVE, dpi=200)
    plt.show(); print()




if __name__ == '__main__':
    run()
