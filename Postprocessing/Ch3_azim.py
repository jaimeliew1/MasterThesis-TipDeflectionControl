# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def get_TD_azim_from_sim(sim):
    channels = {'Azim': 2,
                'RBM1': 26, 'RBM2': 29, 'RBM3': 32,
                'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    for i, seed in enumerate(sim):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim = data.Azim
            td = -data[['TD1', 'TD2', 'TD3']].values
        azim = np.append(azim, data.Azim)
        td = np.append(td, -data[['TD1', 'TD2', 'TD3']].values, 0)

        td -= np.reshape(td.mean(1), [-1, 1])
    return azim, td



def run(dlcs, SAVE=None):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_normal.png'
        SAVE2 = SAVE[:-4] + '_inverse.png'
    else:
        SAVE1 = SAVE2 = None

    _run(dlcs['dlc11_1'], dlcs['dlc11_3'], SAVE=SAVE1)
    _run(dlcs['dlc15_1'], dlcs['dlc15_2'], SAVE=SAVE2)


def _run(dlc1, dlc2, wsp=20, SAVE=None):

    # First row data (ipc04)
    azim1, td1 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc04')[0]
    azim1[0], td1[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc04')[0]
        azim1[amp], td1[amp] = get_TD_azim_from_sim(sim)



    # Second row data (ipc07)
    azim2, td2 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc07')[0]
    azim2[0], td2[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc07')[0]
        azim2[amp], td2[amp] = get_TD_azim_from_sim(sim)


    # Set up plot
    fig, axes = plt.subplots(2, 4, sharey=True, sharex=True, figsize=[6, 4])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)
    axes[0, 0].set_ylim(-6, 6)
    axes[0, 0].set_xticks([0, 120, 240])
    axes[0, 0].set_yticks(np.arange(-4, 6, 2))
    axes[0, 0].autoscale(axis='x')

    hexbinConfig = {'gridsize':30,
                    #'extent':extent,
                    'linewidths':0.25,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':2000}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25

    # labels
    fig.text(0.45, 0.0, 'Azimuth Angle [deg]', ha='center', rotation='horizontal')
    fig.text(0.05, 0.5, 'Tip Deflection [m]', va='center', rotation='vertical')


    x = np.linspace(0, 360, 360)
    y = -np.cos(np.deg2rad(x))
    for i, key in enumerate(azim1.keys()):
        ax = axes[0, i]
        hexPlot = ax.hexbin(azim1[key], td1[key][:, 0], cmap='Blues', **hexbinConfig)
        ax.plot(x, key*y, '--r', lw=1.5)
        ax.annotate('$C_{f1p}$ ' + f'$A_r={i}$' , xy=(0.5, 0.01),
                xycoords='axes fraction', size=10, ha='center', va='bottom',
                bbox=dict(ec='w', fc='w', alpha=0.0))

        ax = axes[1, i]
        hexPlot = ax.hexbin(azim2[key], td2[key][:, 0], cmap='Blues', **hexbinConfig)
        ax.plot(x, key*y, '--r', lw=1.5, label= 'Reference')
        ax.annotate('$C_{2}$, ' + f'$A_r={i}$' , xy=(0.5, 0.01),
                xycoords='axes fraction', size=10, ha='center', va='bottom',
                bbox=dict(ec='w', fc='w', alpha=0.0))

    axes[-1, -1].legend(loc='upper left', bbox_to_anchor=(0.4, -0.1))



    N = len(azim1[0])
    cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist(), pad=0.02)
    cb.set_ticks(np.linspace(0, 2000, 6)) #based on vmin and vmax
    ticklabels = ['{:1.1f}%'.format(x*100) for x in np.linspace(0/N, 2000/N, 6)]
    ticklabels[-1] = '$>$' + ticklabels[-1]
    cb.set_ticklabels(ticklabels)
    cb.ax.tick_params(labelsize=8)
    cb.set_label('Probability of Occurences', labelpad=0)


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()




if __name__ is '__main__':
    dlcs = {
    'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}

    run(dlcs, SAVE=False)