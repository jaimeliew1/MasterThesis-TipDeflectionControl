import numpy as np
from JaimesThesisModule import ControlDesign
# designed to tackle 4m/s at 1p and 2p

def make(F1P=0.095, lead=77.5):
    #lead = 70
    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.32 * 2 * np.pi

    controller.addPolePair([w1p, 2.05*w1p], [0.08, 0.05])
    controller.addZeroPair([2*w1p, 3*w1p], [0.1, 0.5])

    controller.addLeadCompensator(lead, F1P)
    controller.addLeadCompensator(lead, F1P)

    mag, phase = controller.freqResp(F1P)
    controller.K = 1/mag
    controller.K *= 0.1
    print(controller.freqResp(F1P))
    return controller.tf


if __name__ == '__main__':

    C = make()











