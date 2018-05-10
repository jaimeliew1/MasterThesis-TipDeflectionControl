import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from JaimesThesisModule import ControlDesign, PostProc

#from Controllers import ControllerEvaluation

def make(F1P=0.16, lead=77.5):

    controller = ControlDesign.Controller2(Ts=0.01)
    Kp = 0.015
    Ti = 1

    controller.addZero(-1/Ti)
    controller.addPole(0)
    controller.K = Kp

    # RBM controller gain adjustment:
    controller.K *= 3.4e-4

    print(controller.freqResp(F1P))


    return controller.tf

if __name__ == '__main__':

    C = make()












