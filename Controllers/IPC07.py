import numpy as np
from JaimesThesisModule import ControlDesign
# designed to tackle above rated at 1p and 2p
# Note: K = 0.1/mag_ip is unstable at 10m/s and has a high pitch rate.
def make(F1P=0.16, lead=77.5):
    #lead = 70
    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.32 * 2 * np.pi

    controller.addPolePair([w1p, 2.05*w1p], [0.1, 0.1])
    controller.addZeroPair([1.4*w1p, 2.5*w1p], [0.1, 0.3])

    controller.addLeadCompensator(lead, F1P)
    controller.addLeadCompensator(lead, F1P)

    mag, phase = controller.freqResp(F1P)
    controller.K = 1/mag
    controller.K *= 0.05
    print(controller.freqResp(F1P))
    return controller.tf


if __name__ == '__main__':

    C = make()











