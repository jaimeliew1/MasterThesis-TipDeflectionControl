import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from JaimesThesisModule import ControlDesign, PostProc

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

    # RBM controller gain adjustment:
    controller.K *= 3.4e-4

    print(controller.freqResp(F1P))


    return controller.tf

if __name__ == '__main__':

    C = make()












