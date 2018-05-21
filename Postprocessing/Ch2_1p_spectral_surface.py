# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from JaimesThesisModule import PostProc
from Modelling import OLResponse
from scipy import signal, interpolate

Fs = 100

opData = np.array([  [4.0, 0.10],
                     [6.0, 0.10],
                     [8.0, 0.1213],
                     [10.0, 0.1517],
                     [12.0, 0.16],
                     [14.0, 0.16],
                     [16.0, 0.16],
                     [18.0, 0.16],
                     [20.0, 0.16],
                     [22.0, 0.16],
                     [24.0, 0.16],
                     [26.0, 0.16]])



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




def SpectralContour(X, Y, Z, ax=None):
    zmax = 100

    norm = colors.Normalize(vmin=-zmax, vmax=zmax,clip=True)
    levels = np.linspace(-zmax, zmax, 21)
    CP = ax.contourf(X, Y, Z, levels,
                     norm=norm, cmap='RdYlBu_r')
    ax.contour(X, Y, Z, levels, colors='k', linewidths=0.1)

    return CP


def plotRotorFreq(nP=1, ax=None):
    F1p = opData[-1,1]
    if ax is None:
        ax = plt.gca()
    for n in range(nP):
        ax.plot(opData[:,0], (n+1) * opData[:,1], '--', color='k', lw=0.5)
        caption = '$f_{' + f'{n+1}' + 'p}$'
        ax.text(11, 0.01 + F1p*(n+1), caption, color='k')






def run(dlc, dlc_noipc, SAVE=False):
    C = ['ipc04', 'ipc09', 'ipc10', 'ipc11']

    fig, ax = plt.subplots(2, 2, sharex=True, figsize=[8, 6])
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    for i, c in enumerate(C):
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

        ax.ravel()[i].autoscale(tight=True)
        contour = SpectralContour(X, Y, Z, ax.ravel()[i])
        plotRotorFreq(4, ax.ravel()[i])
        ax.ravel()[i].set_yticks([])

        # title (actually an annotation)
        ax.ravel()[i].annotate('$f_{'+f'{i+1}'+'p}$ control' , xy=(0.96, 0.96), xycoords='axes fraction',
                size=10, ha='right', va='top',
                bbox=dict(boxstyle='round', fc='w', alpha=0.7))
    # labels
    fig.text(0.07, 0.5, 'Frequency [Hz]', va='center', rotation='vertical')
    fig.text(0.45, 0.07, 'Wind Speed [m/s]', ha='center', rotation='horizontal')
    # ticks
    ax[0, 0].set_yticks([0.2, 0.4, 0.6, 0.8])
    ax[1, 0].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[0, 0].set_xticks([5, 10, 15, 20, 25])

    #color bar
    CB = fig.colorbar(contour, ax=ax.ravel().tolist())
    CB.set_label('Change in Tip Deflection [\%]',usetex=True)


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()



if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')


    run(dlc, dlc_noipc,SAVE=False)





