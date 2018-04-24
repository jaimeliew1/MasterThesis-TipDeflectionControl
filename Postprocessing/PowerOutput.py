# -*- coding: utf-8 -*-
"""
A module which performs analysis on a certain aspect of the tip deflection
controller results.

This script analyses: Power Output

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from JaimesThesisModule import PostProc


def run(dlc, ref_dlc, c, SAVE=None):
    #%% Violin plot

    key = 'Pelec'; unit = 'W'

    x, y, hue = np.array([]), np.array([]), np.array([])
    sims = ref_dlc(yaw=0)
    N = len(sims[0].seeds[0].Data[key])
    for sim in sims:
        for seed in sim:
            x = np.append(x, np.ones(N)*sim.wsp)
            y = np.append(y, seed.Data[key].values)
            hue = np.append(hue, ['noipc']*N)


    sims = dlc(controller=c, yaw=0, Kp=-1)
    for sim in sims:
        for seed in sim:
            if seed.shutdown:
                continue
            x = np.append(x, np.ones(N)*sim.wsp)
            y = np.append(y, seed.Data[key].values)
            hue = np.append(hue, [c]*N)
    sns.set_style("whitegrid")
    plt.figure(figsize=[7,5])
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('$P_{elec}$ [W]')
    sns.violinplot(x=x, y=y, hue=hue, split=True)
    plt.legend(loc='upper left')
    #


    #Statistics.run(dlc, ref_dlc, save=save, key='Pelec', unit='W')
    if SAVE:
        plt.savefig('../Figures/{}/{}_Power.png'.format(c, c), dpi=200)
    plt.show(); print()




if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc, 'ipc04', SAVE=True)