import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from JaimesThesisModule import ControlDesign, PostProc
from Modelling import BladeModel

#from Controllers import ControllerEvaluation

def make(Kp = 0.015, Ti = 1):

    controller = ControlDesign.Controller2(Ts=0.01)

    controller.addZero(-1/Ti)
    controller.addPole(0)
    controller.K = Kp

    return controller.tf




if __name__ == '__main__':
    wsp = 18
    f1p = 0.16 # hz

    P = BladeModel.Blade(wsp)
    C = make(0.0142, 1.0) # Todo. make this controller sm >= 0.6
    sys = ControlDesign.Turbine(P, C)

    # stability margin
    print('Sm: {:2.3f}\n'.format(sys.sm))

    # performance at f1p to f4p
    for i, perf in enumerate(sys.performance(f1p)):
        print('f{}p: {:+.2f}%'.format(i+1, perf*100))

















