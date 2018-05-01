import numpy as np
from JaimesThesisModule import ControlDesign
# designed to tackle wsp = 10m/s
# Note: K = 0.1/mag_ip is unstable at 10m/s and has a high pitch rate.
def make(F1P=0.125, lead=77.5):
    #lead = 70
    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.25 * 2 * np.pi

    controller.addPolePair([w1p, 2*w1p], [0.08, 0.04])
    controller.addZeroPair([OmegaTOWER, 3*w1p], [0.1, 0.3])

    controller.addLeadCompensator(lead, F1P)
    controller.addLeadCompensator(lead, F1P)

    mag, phase = controller.freqResp(F1P)
    controller.K = 1/mag
    controller.K *= 0.05
    print(controller.freqResp(F1P))
    return controller.tf


if __name__ == '__main__':

    C = make()











