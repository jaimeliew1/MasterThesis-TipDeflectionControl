# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import Analysis, PostProc
from Modelling import BladeModel, OLResponse
from scipy import signal, interpolate

Fs = 100

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

def run(dlc, dlc_noipc, c, save=True):
    Z = []
    WSP = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    Freq = np.linspace(0, 0.8, 1000)
    for wsp in WSP:
        sim = dlc(wsp=wsp, yaw=0, controller=c)
        Ycl = Spectrum(sim[0])
        Yol = OLResponse.Response(wsp)
        Yred = lambda f: 100*(Ycl(f)/Yol(f) - 1)
        Z.append(Yred(Freq))

    X, Y = np.meshgrid(WSP, Freq)
    Z = np.array(Z).T


    fig, ax = plt.subplots()
    ax.autoscale( tight=True)
    ax.set_ylabel('Frequency [Hz]'); ax.set_xlabel('Wind Speed [m/s]')
    Analysis.SpectralContour3(X, Y, Z, ax)
    Analysis.plotRotorFreq(4, ax)
    if save:
        plt.savefig('../Figures/SpectralContour/SpectralContour_{}.png'.format(c), dpi=200)



if __name__ is '__main__':

    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc, 'ipc04', save=True)





