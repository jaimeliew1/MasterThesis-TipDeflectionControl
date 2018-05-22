# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from JaimesThesisModule import Analysis, PostProc, ControlDesign


from Modelling import BladeModel, OLResponse
from Controllers.IPC07 import make

SAVE =True
Fs = 1/0.01




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


def magplotSetup(axes, F1p=None):
    fig, axes = plt.subplots()
    axes.grid('off')
    axes.set_ylabel('Magnitude [dB]')
    axes.set_xlabel('Frequency [Hz]')
    axes.set_xlim(xlim)
    axes.set_xlim([0.01, xlim[1]])
    axes.set_xscale('log')

    axes.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes.set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes.grid(which='minor')

    return fig, axes

def run(dlc, dlc_noipc, SAVE=False):

    F1p = 0.16
    WSP = [6, 12, 18, 24]

    fig, axes = plt.subplots(2, 2, sharey=True, figsize=[8, 6])
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    for wsp, ax in zip(WSP, axes.ravel()):
        # Load transfer functions
        C = make()
        P = BladeModel.Blade(wsp)
        Yol = OLResponse.Response(wsp)

        # Calculate predicted output spectrum
        system = ControlDesign.Turbine(P, C)
        w, H = signal.freqresp(system.S)
        f = w/(2*np.pi)
        Ycl_pred = abs(H)*Yol(f)

        # Load close loop output spectrum
        Sim = dlc(yaw=0, wsp=wsp, controller='ipc07', Kp = -1)[0]
        Ycl = Spectrum(Sim)



        ax.plot(f, Yol(f), label='$Y_{OL}$')
        ax.plot(f, Ycl_pred, '--k', label ='$Y_{CL}$ (predicted)')
        ax.plot(f, Ycl(f), 'r', label ='$Y_{CL}$ (actual)')

        # axis
        ax.set_xscale('log')
        ax.set_xlim(0.05, 1.5)

        # ticks
        ax.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
        ax.grid(axis='x', which='minor')


        # annotate
        ax.annotate(f'WSP=${wsp}m/s$' , xy=(0.5, 0.96), xycoords='axes fraction',
                    size=10, ha='center', va='top',
                    bbox=dict(boxstyle='round', fc='w', alpha=0.0))
    # axis
    ax.set_yscale('log')
    ax.set_ylim(0.001, 1)

    # ticks
    axes[0, 0].set_xticklabels([])
    axes[0, 1].set_xticklabels([])
    axes[1, 0].set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes[1, 1].set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)

    # labels
    fig.text(0.05, 0.5, 'Magnitude [m]', va='center', rotation='vertical')
    fig.text(0.5, 0.07, 'Frequency [Hz]', ha='center', rotation='horizontal')


    axes[1, 1].legend(loc='lower left')
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()


    # print some results
    fnp = 0.16*np.array([1, 2, 3, 4])
    for f in fnp:
        pred = abs(signal.freqresp(system.S, f*2*np.pi)[1][0])*100 - 100
        act = Ycl(f)/Yol(f)*100-100
        print('{:2.2f}%, {:2.2f}%'.format(pred, act))



if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    run(dlc, dlc_noipc, SAVE=False)


