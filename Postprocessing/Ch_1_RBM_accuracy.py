# -*- coding: utf-8 -*-
"""
Analyses the correlation between root bending moment and tip deflection
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import Analysis, PostProc


def run(dlc_noipc, SAVE=None):

    pass
    #return X, Y, coeffs, mean


if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')



    #%% Load rbm and td data
    channels = {'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}

    WSP = np.arange(4, 27, 2)
    X, Y, meanX, meanY = {}, {}, {}, {}
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
        meanX[wsp] = np.mean(X[wsp])
        meanY[wsp] = np.mean(Y[wsp])
#        X[wsp] = np.array(X[wsp]) - np.mean(X[wsp])
#        Y[wsp] = np.array(Y[wsp]) - np.mean(Y[wsp])
    #%% Correlation analysis

    coeffs = {}
    for wsp in WSP:
        coeffs[wsp] = np.polyfit(Y[wsp], X[wsp], 1)
    #%% Find error td~ - td

    wsp = 26
    # using TD sensor for RBM estimation
    X_ = np.polyval(coeffs[wsp], Y[wsp])
    plt.figure()
    plt.hexbin(Y[wsp], X[wsp])
    plt.plot(Y[wsp], X_, '--r', lw=1)

    e = (X_ - X[wsp])
    plt.figure()
    plt.hist(e, 30)
    print(np.std(e))

    # using strain gauge for TD estimation
    a, b = 1/coeffs[wsp][0], -coeffs[wsp][1]/coeffs[wsp][0]
    Y_ = np.polyval([a, b], X[wsp])
    plt.figure()
    plt.hexbin(X[wsp], Y[wsp])
    plt.plot(X[wsp], Y_, '--r', lw=1)

    e = (Y_ - Y[wsp])
    plt.figure()
    plt.hist(e, 30)
    print(np.std(e))

    # table of errors
    eX, eY = {}, {}
    for wsp in WSP:
    # using TD sensor for RBM estimation
        X_ = np.polyval(coeffs[wsp], Y[wsp])
        e = (X_ - X[wsp])
        eX[wsp] = np.std(e)
    # using strain gauge for TD estimation
        a, b = 1/coeffs[wsp][0], -coeffs[wsp][1]/coeffs[wsp][0]
        Y_ = np.polyval([a, b], X[wsp])
        e = (Y_ - Y[wsp])
        eY[wsp] = np.std(e)













    #plt.rc('text', usetex=True)
    #X, Y, coeffs, mean = run(dlc_noipc, SAVE=False)
    #plt.rc('text', usetex=False)
    #%%
#    WSP = np.arange(4, 27, 2)
#    e = {}
#    #mean, std = [], []
#    eperc = {}
#    for wsp in WSP:
#        Y_ = np.polyval(coeffs[wsp], X[wsp])
#        e[wsp] = Y_ - Y[wsp]
#
#        #mean.append(np.mean(e[wsp]))
#        #std.append(np.std(e[wsp]))
#        eperc[wsp] = np.std(e[wsp])/mean[wsp]
#        print(f'wsp: {wsp:2}\t std: {np.std(e[wsp]):2.2f}kNm')
#
#    # print in latex compatible form
#    for wsp in [6, 12, 18, 24]:
#        print(f'{wsp:2} & {np.std(e[wsp]):2.2f} \\\\')








