# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc, dlc_noipc, C, SAVE=False):
    C = ['ipc04', 'ipc05', 'ipc06', 'ipc07', 'ipc08']
    C = ['ipc04', 'ipc05', 'ipc06']
    keys = ['RBM1', 'RBMe1', 'MBx', 'MBy']
    titles = ['Flapwise blade RBM', 'Edgewise blade RBM',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])

    # for eack key and title, make a new bar graph.
    for key, title in zip(keys, titles):
        Req_ol, Req_cl = [0]*12, np.zeros([len(C), 12])

        for i, wsp in enumerate(WSP):
            sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
            Req_ol[i] = float(sim_ref.Req[key])

            for j, c in enumerate(C):
                sim = dlc(wsp=wsp, yaw=0, controller=c)[0]
                Req_cl[j, i] = float(sim.Req[key])

       # bar graph
        width = 1.4/(len(C) + 1)

        fig, ax = plt.subplots()
        ax.set_ylabel('$R_{eq}$ [kNm]')
        ax.set_xlabel('Wind Speed [m/s]')
        ax.set_xticks(np.arange(4, 27, 2))
        ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0')
        for j, c in enumerate(C):
            ax.bar(WSP + width*(j+1), Req_cl[j], width, label=c, ec='0')
        ax.set_title(title)
        ax.legend()
        if SAVE:
            plt.savefig('../Figures/{}/{}_FatigueLoads_{}.png'.format(c,c, key), dpi=200)
        plt.show(); print()




if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):
        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc, 0, SAVE=False)


