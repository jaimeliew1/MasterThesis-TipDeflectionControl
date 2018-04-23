import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from JaimesThesisModule import ControlDesign, PostProc
#from Modelling import BladeModel, spectrum_td
#from Controllers import ControllerEvaluation
# All turbines shutdown :(


def make(F1P=0.16, lead=80):

    controller = ControlDesign.Controller2(Ts=0.01)
    w1p = F1P *2*np.pi
    OmegaTOWER =  0.25 * 2 * np.pi

    controller.addPolePair([w1p, 2*w1p, 3*w1p], [0.08, 0.08, 0.03])
    controller.addZeroPair([1.6*w1p, w1p*3.5, w1p*4.2], [0.1, 0.05, 0.04])

    controller.addLeadCompensator(lead, F1P)
    controller.addLeadCompensator(lead, F1P)

    mag, phase = controller.freqResp(F1P)
    controller.K = 1/mag
    controller.K *= 0.1

    # This is the optimised controller from matlab. tidy this up
    #b, a = np.loadtxt('C_ncfsyn.csv', delimiter=',')
    cOpt = signal.TransferFunction(0.7*np.array([  2.97790000e-01,   1.07970000e+00,   1.46430000e+01,
         3.39710000e+01,   2.26140000e+02,   3.11770000e+02,
         1.20350000e+03,   9.17170000e+02,   1.54850000e+03,
         1.14090000e+03,  -5.21350000e+02]), np.array([  1.00000000e+00,   3.78540000e+01,   3.49290000e+02,
         2.07530000e+03,   1.20140000e+04,   2.70120000e+04,
         1.16730000e+05,   1.11690000e+05,   3.53520000e+05,
         1.11840000e+05,   2.41180000e+05]))
    return cOpt

    return controller.tf


if __name__ == '__main__':
    # Load data if not loaded already
    if ('dlc_noipc' not in locals()):
        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

    C = make()


    ControllerEvaluation.run(C, dlc_noipc, wsp=20)
#    # load openloop output
#    Yol = spectrum_td.openloopSpectrum(dlc_noipc, 18)
#    C = make(lead=80)
#
#    b, a = np.loadtxt('C_ncfsyn.csv', delimiter=',')
#    cOpt = signal.TransferFunction(b, a)
#
#    P = BladeModel.modelTransferFunctions()[6]
#
#    sys = ControlDesign.Turbine(P, C)
#    sys2 = ControlDesign.Turbine(P, cOpt)
#
#    ControlDesign.bode(sys.P, sys.CL, sys2.CL, title='Open and close loop bode plots', F1p=0.16)
#    ControlDesign.bode(sys.S, sys2.S, F1p=0.16, title='Sensitivity function')
#    ControlDesign.bode(sys.L, sys2.L, F1p=0.16, title='Loop Transfer Function')
#    ControlDesign.bode(sys.C, sys2.C, F1p=0.16, title='Controller Transfer Function')
#    ControlDesign.nyquist(sys.L)
#    ControlDesign.nyquist(sys.L, zoom=[-1.5, 1.5])
#
#    ControlDesign.nyquist(sys2.L)
#    ControlDesign.nyquist(sys2.L, zoom=[-1.5, 1.5])
#
#    # Plot openloop and predicted closeloop output spectra
#    fig, ax = plt.subplots()
#
#    ax.set_title('open and close loop output')
#    ax.set_ylabel('Magnitude')
#    ax.set_xlabel('Frequency [Hz]')
#    ax.set_xscale('log')
#    ax.set_yscale('log')
#
#    for i in range(4):
#        ax.axvline(x=0.16*(i+1), linestyle='--',color='k', lw=1)
#
#    w, H = signal.freqresp(sys.S)
#    f = w/(2*np.pi)
#
#    w2, H2 = signal.freqresp(sys2.S)
#    f2 = w2/(2*np.pi)
#
#    ax.plot(f, Yol(f))
#    ax.plot(f, abs(H)*Yol(f))
#    ax.plot(f2, abs(H2)*Yol(f2))
#    ax.set_xlim([0.02, 1.5])
#    ax.set_ylim([0.001, 1])
#    plt.show()
#    print(sys.sm, sys2.sm)

    #%% discretise optimised controller and save to htc
    bz, az = signal.bilinear(C.num, C.den, 100)

    #ControlDesign.saveHTC(bz, az, 'ipc05.htc')










