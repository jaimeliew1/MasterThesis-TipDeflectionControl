# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc, dlc_noipc, SAVE=False):
    dlc2 = PostProc.DLC('dlc11_2')
    C, C2 = 'ipcpi', 'ipc_rbmpi'
    keys = ['RBMf', 'MBt', 'MBy']
    titles = ['Blade (flapwise)',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    labels = ['$C_{PI}$', '$C_{RBM PI}$']
    #WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
    WSP = np.arange(4, 27, 4)
    fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=[10,3])
    plt.subplots_adjust(wspace=0.05)
    # for eack key and title, make a new bar graph.
    for key, title, ax in zip(keys, titles, axes.ravel()):
        Req_ol, Req = [0]*len(WSP), np.zeros([len(C), len(WSP)])
## TO DO I AM TO TIRED
        for i, wsp in enumerate(WSP):
            sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
            Req_ol[i] = float(sim_ref.data[key])

            for j, c in enumerate(C):
                sim = dlc(wsp=wsp, yaw=0, controller=c)[0]
                Req_cl[j, i] = float(sim.data[key])

       # bar graph
        width = 3/(len(C) + 1)


        ax.set_xticks(WSP + 1)
        ax.set_xticklabels(WSP)
        ax.grid(True, axis='y')
        ax.set_axisbelow(True)
        ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0')
        for j, c in enumerate(C):
            ax.bar(WSP + width*(j+1), Req_cl[j], width, label=labels[j], ec='0')
        ax.annotate(title , xy=(0.5, 0.97), xycoords='axes fraction',
                size=10, ha='center', va='top',
                bbox=dict(ec='w', fc='w', alpha=0.7))




# labels
    fig.text(0.06, 0.5, 'Equivalent Bending Moment [kNm]', va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'Wind Speed [m/s]', ha='center', rotation='horizontal')
    axes.ravel()[1].legend(ncol=4,bbox_to_anchor=(1.3, 1.2))
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()




if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    run(dlc, dlc_noipc, SAVE=False)



