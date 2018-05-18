# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""

from Controllers import ControllerEvaluation
from Modelling import BladeModel
from JaimesThesisModule import ControlDesign
from Controllers.IPC_PI import make

def run(dlc=None, dlc_noipc=None, SAVE=None):
    wsp =  18
    C = make()
    P = BladeModel.Blade(wsp)
    sys = ControlDesign.Turbine(P, C)

    ControllerEvaluation.plot_S(sys.S, ylim=[-25, 10], save=SAVE)

if __name__ == '__main__':
    run()

