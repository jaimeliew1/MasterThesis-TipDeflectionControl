'''
Todo: plot PSDs of different wind speeds over each other.

'''
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from JaimesThesisModule import PostProc


def run(dlc_noipc, SAVE=False):

    wsp = 18; F1p = 0.16
    channels =  {'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    Ys = []
    for seed in dlc_noipc(wsp=wsp)[0]:
        data = seed.loadFromSel(channels)
        for key in ['TD1', 'TD2', 'TD3']:
            f, Py = signal.welch(data[key], 100, nperseg=1024*8)
            Ys.append(Py)
    Yave = np.mean(Ys, axis=0)



    fig, axes = plt.subplots()

    axes.set_ylabel('Power Spectran Density [$m^2$/$Hz$]')
    axes.set_xlabel('Frequency [$Hz$]')
    axes.set_xlim([0.01, 1.5])
    axes.set_xscale('log')
    axes.set_yscale('log')
    axes.set_ylim(0.01, 100)

    axes.set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes.set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)
    axes.grid(which='minor', axis='x')
    axes.grid(axis='y')
    axes.plot(f, Yave)

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
        plt.show(); print()





if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    run(dlc_noipc, SAVE=False)


