# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc, dlc2, dlc_noipc, C, SAVE=False):
    C = 'ipc05'
    C2 = 'ipc_rbm05'
    keys = ['RBMf', 'RBMe', 'MBt', 'MBy']
    titles = ['Flapwise blade RBM', 'Edgewise blade RBM',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])

    # for eack key and title, make a new bar graph.
    for key, title in zip(keys, titles):
        Req_ol, Req_cl, Req_RBM = [0]*12, [0]*12, [0]*12

        for i, wsp in enumerate(WSP):
            sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
            Req_ol[i] = float(sim_ref.data[key])

            sim = dlc(wsp=wsp, yaw=0, controller=C)[0]
            Req_cl[i] = float(sim.data[key])


            sim = dlc2(wsp=wsp, yaw=0, controller=C2)[0]
            Req_RBM[i] = float(sim.data[key])

       # bar graph
        width = 1.4/3

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.15)
        ax.set_ylabel('$R_{eq}$ [kNm]')
        ax.set_xlabel('Wind Speed [m/s]')
        ax.set_xticks(np.arange(4, 27, 2))
        ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0', lw=0.8)

        ax.bar(WSP + width, Req_cl, width, label='TD Control', ec='0', fc='tab:blue')

        ax.bar(WSP + 2*width, Req_RBM, width, label='RBM Control', ec='0', lw=0.8, fc= 'tab:red')
        ax.set_title(title)
        ax.legend()
        if SAVE:
            plt.savefig('../Figures/RBM_vs_TD_control/{}_FatigueLoads_{}.png'.format(C, key), dpi=200)
        plt.show(); print()




if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis()

    dlc = PostProc.DLC('dlc11_1')
    dlc.analysis()

    dlc2 = PostProc.DLC('dlc11_2')
    dlc2.analysis()

    run(dlc, dlc2, dlc_noipc, 0, SAVE=True)



