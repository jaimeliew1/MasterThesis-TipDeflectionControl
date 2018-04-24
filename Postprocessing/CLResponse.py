# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from JaimesThesisModule import Analysis, PostProc, ControlDesign

from Controllers import IPC04, IPC05
from Modelling import BladeModel, OLResponse


SAVE =True
Fs = 1/0.01



def Spectrum(sim):
    Ys = []
    for seed in sim:
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)
            f, Py = signal.welch(seed.Data[key], Fs, nperseg=1024*8)
            Ys.append(np.sqrt(Fs*Py/60000))

    Yave = np.mean(Ys, axis=0)
    Yol = interpolate.interp1d(f, Yave, kind='linear', bounds_error=False)

    return Yol


def magplotSetup(xlim = [0.01, 1.5], F1p=None):
    fig, axes = plt.subplots()
    axes.grid('off')
    axes.set_ylabel('Magnitude [dB]')
    axes.set_xlabel('Frequency [Hz]')
    axes.set_xlim(xlim)
    axes.set_xlim([0.01, xlim[1]])
    axes.set_ylim([1e-3, 1])
    axes.set_xscale('log')
    axes.set_yscale('log')

    # draw f_np lines
    if F1p is not None:
        for i in [1, 2, 3, 4]:
            axes.axvline(F1p*i, linestyle='--',color='k', lw=1)

    return fig, axes

if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    wsp = 18

    # Load transfer functions
    C = IPC04.make()
    P = BladeModel.Blade(wsp)
    Yol = OLResponse.Response(wsp)
    # Calculate predicted output spectrum
    system = ControlDesign.Turbine(P, C)
    w, H = signal.freqresp(system.S)
    f = w/(2*np.pi)
    Ycl_pred = abs(H)*Yol(f)
    # Load close loop output spectrum
    Sim = dlc(yaw=0, wsp=wsp, controller='ipc04', Kp = -1)[0]
    Ycl = Spectrum(Sim)

    fig, ax = magplotSetup(F1p=0.16)
    ax.set_ylabel('Magnitude [m]')
    ax.plot(f, Yol(f), label='$Y_{OL}$')
    ax.plot(f, Ycl_pred, '--k', label ='$Y_{CL}$ (predicted)')
    ax.plot(f, Ycl(f), 'r', label ='$Y_{CL}$ (actual)')
    ax.set_xlim(f.min(), 1.5)
    ax.set_title('wsp = {}m/s'.format(wsp))
    ax.legend()

    if SAVE:
        plt.savefig('../Figures/CLResponse/TipDeflection_Spectrum_{}.png'.format(wsp), dpi=200)
    plt.show();print()
