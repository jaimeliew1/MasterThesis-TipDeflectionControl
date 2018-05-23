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
    X, Y = {}, {}
    for wsp in WSP:
        X[wsp], Y[wsp] = [], []
        for seed in dlc_noipc(wsp=wsp, controller='ipc07')[0]:
            data = seed.loadFromSel(channels=channels)
            X[wsp] += list(data.RBM1)
            X[wsp] += list(data.RBM2)
            X[wsp] += list(data.RBM3)

            Y[wsp] += list(-data.TD1)
            Y[wsp] += list(-data.TD2)
            Y[wsp] += list(-data.TD3)

        # subtract the mean
        X[wsp] = np.array(X[wsp]) - np.mean(X[wsp])
        Y[wsp] = np.array(Y[wsp]) - np.mean(Y[wsp])
    #%% Correlation analysis
    coeffs = {}
    for wsp in WSP:
        coeffs[wsp] = np.polyfit(X[wsp], Y[wsp], 1)
    #%% Find error td~ - td







    return X, Y, coeffs

if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_1')
    #plt.rc('text', usetex=True)
    X, Y, coeffs = run(dlc_noipc, SAVE=False)
    #plt.rc('text', usetex=False)
    #%%
    WSP = np.arange(4, 27, 2)
    e = {}
    mean, std = [], []
    for wsp in WSP:
        Y_ = np.polyval(coeffs[wsp], X[wsp])
        e[wsp] = Y_ - Y[wsp]
        mean.append(np.mean(e[wsp]))
        std.append(np.std(e[wsp]))

        print(f'wsp: {wsp:2}\t std: {np.std(e[wsp]):2.2f}m')







