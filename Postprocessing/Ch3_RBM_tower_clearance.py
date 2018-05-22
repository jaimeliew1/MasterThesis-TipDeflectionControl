# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from JaimesThesisModule import PostProc

channels = {    'RBM1'      : 26,   # flapwise rbm [kNm]
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,   #Tip deflection - blade 1 [m]
                'TD2'       : 52,
                'TD3'       : 55}



def run(dlc_noipc, dlc, dlc2, wsp=26, SAVE=False):
    #%% Load data into list of x
    X, Y, Z = [], [], []


    Sims = dlc_noipc(wsp=wsp)[0]
    for seed in Sims:
        data = seed.loadFromSel(channels=channels)
        X += list(data.TD1)
        X += list(data.TD2)
        X += list(data.TD3)


    Sims = dlc(wsp=wsp, controller='ipc04')[0]
    for seed in Sims:
        data = seed.loadFromSel(channels=channels)
        Y += list(data.TD1)
        Y += list(data.TD2)
        Y += list(data.TD3)


    Sims = dlc2(wsp=wsp, controller='ipc_rbm04')[0]
    for seed in Sims:
        data = seed.loadFromSel(channels=channels)
        Z += list(data.TD1)
        Z += list(data.TD2)
        Z += list(data.TD3)

    print('mean', np.mean(X), np.mean(Y), np.mean(Z))
    print('std', np.std(X), np.std(Y), np.std(Z))
    print('max', np.max(X), np.max(Y), np.max(Z))
    print('mein', np.min(X), np.min(Y), np.min(Z))

    plt.figure()
    plt.hist(X, 30, range=[-10, 5])
    plt.figure()
    plt.hist(Y, 30, range=[-10, 5])
    plt.figure()
    plt.hist(Z, 30, range=[-10, 5])






    if SAVE:
        plt.savefig(SAVE, dpi=300, bbox_inches='tight')
    plt.show(); print()





if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')
    dlc2 = PostProc.DLC('dlc11_2')


    run(dlc_noipc, dlc, dlc2, SAVE=False)





