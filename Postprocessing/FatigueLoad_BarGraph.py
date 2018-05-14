# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc, dlc_noipc, c, SAVE=False):
    keys = ['RBMf', 'RBMe', 'MBt', 'MBy']
    titles = ['Flapwise blade RBM', 'Edgewise blade RBM',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])

    # for eack key and title, make a new bar graph.
    for key, title in zip(keys, titles):
        Req_ol, Req_cl = [0]*12, [0]*12

        for i, wsp in enumerate(WSP):
            sim = dlc(wsp=wsp, yaw=0, controller=c)[0]
            Req_cl[i] = float(sim.data[key])

            sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
            Req_ol[i] = float(sim_ref.data[key])

       # bar graph
        width = 0.7

        fig, ax = plt.subplots()
        ax.set_ylabel('$R_{eq}$ [kNm]')
        ax.set_xlabel('Wind Speed [m/s]')
        ax.set_xticks(np.arange(4, 27, 2))
        ax.bar(WSP, Req_ol, width, label = 'No control')
        ax.bar(WSP + width, Req_cl, width, label = 'With control')
        ax.set_title(title)
        ax.legend()
        if SAVE:
            plt.savefig('../Figures/{}/{}_FatigueLoads_{}.png'.format(c,c, key), dpi=200)
        plt.show(); print()




if __name__ is '__main__':


    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis()

    dlc = PostProc.DLC('dlc11_1')
    dlc.analysis()

    run(dlc, dlc_noipc, 'ipc07', SAVE=False)



