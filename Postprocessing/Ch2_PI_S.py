# -*- coding: utf-8 -*-
"""
todo: plot multiple sensitivity functions on same plot for different
wind speeds.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from Controllers import ControllerEvaluation
from Modelling import BladeModel, OLResponse
from JaimesThesisModule import ControlDesign, PostProc
from Controllers.IPC_PI import make


Fs = 100


def Spectrum(sim):
    Ys = []
    channels =  {'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    for seed in sim:
        data = seed.loadFromSel(channels)
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)
            f, Py = signal.welch(data[key], Fs, nperseg=1024*8)
            Ys.append(np.sqrt(Fs*Py/60000))

    Yave = np.mean(Ys, axis=0)
    Yol = interpolate.interp1d(f, Yave, kind='linear', bounds_error=False)

    return Yol





def run(dlc=None, dlc_noipc=None, SAVE=None):
    f = np.linspace(0, 1.5, 1000)[1:]

    Yol = OLResponse.Response(18)
    Ycl = Spectrum(dlc(wsp=18, controller='ipcpi')[0])
    C = make()
    P = BladeModel.Blade(18)
    sys = ControlDesign.Turbine(P, C)
    mag = signal.bode(sys.S, w=f*(2*np.pi))[1]
    actualMag = 20*np.log10(Ycl(f)/Yol(f))
    fig, ax = ControllerEvaluation.magplotSetup(F1p=0.16)
    ax.set_xlim(0.05, 1.5)


    ax.axhline(0, lw=1, c='0.8', ls='-')
    ax.plot(f, mag, label='$S(C_{PI})$')
    ax.plot(f, actualMag, '--', label='Actual $S(C_{PI})$')




    ax.set_ylim(-10, 10)
    ax.legend(loc='upper left')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()

if __name__ == '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')
    run(dlc, dlc_noipc)

