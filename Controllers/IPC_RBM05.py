import numpy as np
from JaimesThesisModule import ControlDesign


def make(F1P=0.16, lead=77.5):

    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.25 * 2 * np.pi

    controller.addPolePair([w1p, 2*w1p, 4*w1p], [0.05, 0.05, 0.008])
    controller.addZeroPair([OmegaTOWER, w1p*3.5, w1p*4.2], [0.1, 0.05, 0.04])

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











