# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""

from Controllers import ControllerEvaluation
from Modelling import BladeModel
from JaimesThesisModule import ControlDesign
from Controllers.IPC07 import make

def run(dlc=None, dlc_noipc=None, SAVE=None):
    wsp =  18
    C = make()
    P = BladeModel.Blade(wsp)
    sys = ControlDesign.Turbine(P, C)

    #ControllerEvaluation.plot_nyquist(sys.L, zoom=1.5, rightticks = True, save=SAVE)
    ControllerEvaluation.plot_L(sys.L, margins=True, save=SAVE)


if __name__ == '__main__':
    run()

