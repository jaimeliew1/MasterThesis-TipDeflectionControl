# -*- coding: utf-8 -*-
"""
Analyses the correlation between root bending moment and tip deflection
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import Analysis, PostProc


def run(dlc_noipc, SAVE=None):
    #%% Load rbm and td data

    channels = {'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}

    WSP = np.arange(4, 27, 2)
    X, Y, mean = {}, {}, {}
    for wsp in WSP:
        X[wsp], Y[wsp] = [], []
        for seed in dlc_noipc(wsp=wsp)[0]:
            data = seed.loadFromSel(channels=channels)
            X[wsp] += list(data.RBM1)
            X[wsp] += list(data.RBM2)
            X[wsp] += list(data.RBM3)

            Y[wsp] += list(-data.TD1)
            Y[wsp] += list(-data.TD2)
            Y[wsp] += list(-data.TD3)

        # subtract the mean
        mean[wsp] = np.mean(X[wsp])
        X[wsp] = np.array(X[wsp]) - np.mean(X[wsp])
        Y[wsp] = np.array(Y[wsp]) - np.mean(Y[wsp])
    #%% Correlation analysis
    X, Y = Y, X
    coeffs = {}
    for wsp in WSP:
        coeffs[wsp] = np.polyfit(X[wsp], Y[wsp], 1)
    #%% Find error td~ - td







    return X, Y, coeffs, mean

if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    #plt.rc('text', usetex=True)
    X, Y, coeffs, mean = run(dlc_noipc, SAVE=False)
    #plt.rc('text', usetex=False)
    #%%
    WSP = np.arange(4, 27, 2)
    e = {}
    #mean, std = [], []
    eperc = {}
    for wsp in WSP:
        Y_ = np.polyval(coeffs[wsp], X[wsp])
        e[wsp] = Y_ - Y[wsp]

        #mean.append(np.mean(e[wsp]))
        #std.append(np.std(e[wsp]))
        eperc[wsp] = np.std(e[wsp])/mean[wsp]
        print(f'wsp: {wsp:2}\t std: {np.std(e[wsp]):2.2f}kNm')

    # print in latex compatible form
    for wsp in [6, 12, 18, 24]:
        print(f'{wsp:2} & {np.std(e[wsp]):2.2f} \\\\')








