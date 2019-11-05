import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from JaimesThesisModule import ControlDesign, PostProc
from Modelling import BladeModel

#from Controllers import ControllerEvaluation

def make(F1P=0.16, lead=77.5):

    controller = ControlDesign.Controller2(Ts=0.01)
    Omega1P = F1P *2*np.pi

    controller.addPolePair(Omega1P, 0.05)
    controller.addLeadCompensator(lead, F1P)
    controller.addLeadCompensator(lead, F1P)

    mag, phase = controller.freqResp(F1P)
    controller.K = 1/mag
    controller.K *= 0.1


    return controller.tf

if __name__ == '__main__':
    wsp = 18
    f1p = 0.16 # hz

    for wsp in np.arange(4, 27, 2):
        print('\n\nwsp: ', wsp)
        P = BladeModel.Blade(wsp)
        C = make()
        sys = ControlDesign.Turbine(P, C)

        # stability margin
        print('Sm: {:2.3f}\n'.format(sys.sm))

        # performance at f1p to f4p
        for i, perf in enumerate(sys.performance(f1p)):
            print('f{}p: {:+.2f}%'.format(i+1, perf*100))
