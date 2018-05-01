import numpy as np
from JaimesThesisModule import ControlDesign
# designed to tackle above rated at 2p

def make(F1P=0.16, lead=50):
    #lead = 70
    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.32 * 2 * np.pi

    controller.addPolePair([2.05*w1p], [0.05])
    controller.addZeroPair([2.8*w1p], [ 0.7])

    controller.addLeadCompensator(lead, 3*F1P)
    controller.addLeadCompensator(lead, 3*F1P)

    mag, phase = controller.freqResp(2*F1P)
    controller.K = 1/mag
    controller.K *= 0.05
    print(controller.freqResp(2*F1P))
    return controller.tf


if __name__ == '__main__':

    C = make()











