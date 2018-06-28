# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from JaimesThesisModule import PostProc
Fs = 100
F1p = 0.16

def freqResp(x, Fs, fmax=None):
    f  = np.linspace(0, Fs, len(x))
    Y = 2*abs(np.fft.fft(x))/len(x)

    if fmax:
        Y = Y[f <= fmax]
        f = f[f <= fmax]
    return f, Y



def magplotSetup(xlim = [0.01, 1.5], F1p=None):


    axes.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes.set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes.grid(which='minor', axis='x')

    return fig, axes




def OLFreqResp(wsp, dlc_noipc, smooth=False):
    sim = dlc_noipc(yaw=0, wsp=wsp)[0]
    Ys = []
    channels =  {'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    for seed in sim:
        data = seed.loadFromSel(channels)
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)

            if not smooth:
                f, Y = freqResp(data[key], Fs, fmax=10)
                Ys.append(Y)

            if smooth:
                f, Py = signal.welch(data[key], Fs, nperseg=1024*8)
                Ys.append(np.sqrt(Fs*Py/60000))

    Yave = np.mean(Ys, axis=0)
    return f, Yave


def run(SAVE=False):
# Load HAWC2 result data
    dlc_noipc = PostProc.DLC('dlc11_0')

    #WSP = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    WSP = [6, 12, 18, 24]
    fig, axes = plt.subplots(2, 2, sharey=True, figsize=[8, 6])
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    for wsp, ax in zip(WSP, axes.ravel()):


        f, Y = OLFreqResp(wsp, dlc_noipc)
        f_, Y_ = OLFreqResp(wsp, dlc_noipc, smooth=True)
        ax.plot(f, Y, label='Mean Fourier Transform')
        ax.plot(f_, Y_, label='Smoothed Fourier Transform')
    # axis
        ax.set_xscale('log')
        ax.set_xlim(0.05, 1.5)

        # ticks
        ax.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
        ax.grid(axis='x', which='minor')


        # annotate
        ax.annotate(f'$U={wsp}m/s$' , xy=(0.5, 0.96), xycoords='axes fraction',
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



if __name__ is '__main__':
    run()