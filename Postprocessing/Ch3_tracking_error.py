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



def run(dlcs, wsp = 20, SAVE=None):


    ##### normal shear #####
    dlc1, dlc2 = dlcs['dlc11_1'], dlcs['dlc11_3']

    # First row data (ipc04)
    azim1, td1 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc04')[0]
    azim1[0], td1[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3, 4]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc04')[0]
        azim1[amp], td1[amp] = get_TD_azim_from_sim(sim)



    # Second row data (ipc07)
    azim2, td2 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc07')[0]
    azim2[0], td2[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3, 4]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc07')[0]
        azim2[amp], td2[amp] = get_TD_azim_from_sim(sim)



    ##### inverse shear #####
    dlc1, dlc2 = dlcs['dlc15_1'], dlcs['dlc15_2']

    # First row data (ipc04)
    azim3, td3 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc04')[0]
    azim3[0], td3[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3, 4]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc04')[0]
        azim3[amp], td3[amp] = get_TD_azim_from_sim(sim)



    # Second row data (ipc07)
    azim4, td4 = {}, {}
    # get data for Ar = 0
    sim = dlc1(wsp=wsp, controller='ipc07')[0]
    azim4[0], td4[0] = get_TD_azim_from_sim(sim)

    # get data for Ar = 1, 2, 3
    for amp in [1, 2, 3, 4]:
        sim = dlc2(wsp=wsp, _amp=amp, controller='ipc07')[0]
        azim4[amp], td4[amp] = get_TD_azim_from_sim(sim)


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')


    data = [[azim1, td1],
            [azim2, td2],
            [azim3, td3],
            [azim4, td4],]
    labels = ['$C_{f1p}$ Normal shear',
              '$C_{2}$ ~~~Normal shear',
              '$C_{f1p}$ Inverse shear',
              '$C_{2}$ ~~~Inverse shear',]
    styles = ['--', '--', '-', '-']
    colors = ['tab:blue', 'tab:orange', 'tab:blue', 'tab:orange',]
    amps = [0, 1, 2, 3, 4]
    plt.figure(figsize=[5, 3])

    for i, (azim, td) in enumerate(data):

        std = []

        for amp in amps:
            target = -amp*np.cos(np.deg2rad(azim[amp]))
            std.append((target-td[amp][:,0]).std())
        plt.plot(amps, std, styles[i], c = colors[i], label=labels[i])
        print(std)
    plt.legend(ncol=2, loc='upper left')
    plt.xlim(0, 4)
    plt.xticks(amps)
    plt.xlabel('Tip Tracking Amplitude, $A_r$ [m]')
    plt.ylabel('Standard Deviation of Tracking Error [m]')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()





if __name__ is '__main__':
    if 'dlcs' not in locals():
        print('loading data...')
        dlcs = {
        'dlc11_0':PostProc.DLC('dlc11_0'),
        'dlc11_1':PostProc.DLC('dlc11_1'),
        'dlc11_3':PostProc.DLC('dlc11_3'),
        'dlc15_0':PostProc.DLC('dlc15_0'),
        'dlc15_1':PostProc.DLC('dlc15_1'),
        'dlc15_2':PostProc.DLC('dlc15_2')}
    plt.rc('text', usetex=True)
    run(dlcs, SAVE=False)

