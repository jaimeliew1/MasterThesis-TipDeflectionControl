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
        for seed in dlc_noipc(wsp=wsp)[0]:
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
    coeffs, corr = {}, {}
    for wsp in WSP:
        coeffs[wsp] = np.polyfit(X[wsp], Y[wsp], 1)
        corr[wsp] = np.corrcoef(X[wsp], Y[wsp])[0,1]
    #%% Plot
    def corrPlot(ax, X, Y, wsp):
        hexbinConfig = {'gridsize':40,
                        'linewidths':1,
                        'mincnt':1,
                        'vmin':0,
                        'vmax':5400,
                        'extent': [-15000, 15000, -8, 8],
                        'cmap':'Blues'}
        if SAVE:
            hexbinConfig['linewidths'] = 0.25
        coeffs = np.polyfit(X, Y, 1)
        corr = np.corrcoef(X, Y)[0,1]
        xline = np.linspace(-15000, 15000)
        yline = np.polyval(coeffs, xline)
        hexPlot = ax.hexbin(X, Y, **hexbinConfig)
        ax.plot(xline, yline, '--r', lw=1)

        # text
        string = '$R^2= {:2.2f}$\n$Slope = {:2.2E} m/Nm$'.format(corr**2,
                        coeffs[0]/1000)
        string = string.replace('E-0', '\\times 10^{-')
        string = string.replace(' m', '} m')
        ax.text(0.35, 0.9, f'$WSP={wsp}m/s$', transform=ax.transAxes)
        ax.text(0.2, 0.03, string, transform=ax.transAxes, color='k')

        return hexPlot




    fig, axes = plt.subplots(2, 2, figsize=[8,6], sharex=True, sharey=True)
    plt.subplots_adjust(left=0.1, wspace=0.05, hspace=0.05)
    for wsp, ax  in zip([6, 12, 18, 24], axes.ravel()):
        hexPlot = corrPlot(ax, X[wsp], Y[wsp], wsp)

    # labels
    fig.text(0.04, 0.5, 'Flapwise Tip Deflection [m]', va='center', rotation='vertical')
    fig.text(0.5, 0.04, 'Root Bending Moment [kNm]', ha='center', rotation='horizontal')
    # ticks
    axes[0, 0].set_yticks(np.arange(-6, 7, 2))
    axes[0,0].set_xticks(np.arange(-15000, 15000, 5000))
    # colorbar

    N = len(X[4])
    cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist())
    cb.set_ticks(np.linspace(0, 5400, 6)) #based on vmin and vmax
    ticklabels = ['{:1.1f}\\%'.format(x*100) for x in np.linspace(0/N, 5400/N, 6)]
    ticklabels[-1] = '$>$' + ticklabels[-1]
    cb.set_ticklabels(ticklabels)
    cb.set_label('Probability of Occurences')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()

if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    plt.rc('text', usetex=True)
    run(dlc_noipc, SAVE=True)
    plt.rc('text', usetex=False)


