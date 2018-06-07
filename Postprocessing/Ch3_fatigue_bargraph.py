# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlcs, SAVE=None):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_normal_ipc04.png'
        SAVE2 = SAVE[:-4] + '_normal_ipc07.png'
        SAVE3 = SAVE[:-4] + '_inverse_ipc04.png'
        SAVE4 = SAVE[:-4] + '_inverse_ipc07.png'
    else:
        SAVE1 = SAVE2 = SAVE3 = SAVE4= None
    _run(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'], c='ipc04', SAVE=SAVE1)
    _run(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'], c='ipc07', SAVE=SAVE2)
    _run(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'], c='ipc04',SAVE=SAVE3)
    _run(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'], c='ipc07',SAVE=SAVE4)



def _run(dlc_noipc, dlc, dlc2, c='ipc04', SAVE=False):
    A = [1, 2, 3]
    keys = ['RBMf', 'MBt', 'MBy']
    titles = ['Blade (flapwise)',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    labels = ['$A_r=1$', '$A_r=2$', '$A_r=3$']

    WSP = np.arange(4, 27, 4)
    fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=[10,3])
    plt.subplots_adjust(wspace=0.05)
    # for eack key and title, make a new bar graph.
    for key, title, ax in zip(keys, titles, axes.ravel()):
        Req_ol, Req_0, Req_cl = [0]*len(WSP), [0]*len(WSP), np.zeros([len(A), len(WSP)])

        for i, wsp in enumerate(WSP):
            sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
            Req_ol[i] = float(sim_ref.data[key])

            sim = dlc(wsp=wsp, controller=c)[0]
            Req_0[i] = float(sim.data[key])

            for j, amp in enumerate(A):
                sim = dlc2(wsp=wsp, _amp=amp, controller=c)[0]
                Req_cl[j, i] = float(sim.data[key])

       # bar graph
        width = 3/(len(A) + 2)
        #http://colorbrewer2.org/#type=sequential&scheme=YlGnBu&n=4
        colors = ['#ffffcc','#a1dab4','#41b6c4','#225ea8']

        ax.set_xticks(WSP + 1)
        ax.set_xticklabels(WSP)
        ax.grid(True, axis='y')
        ax.set_axisbelow(True)
        ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0')
        ax.bar(WSP + width, Req_0, width, label = '$A_r=0$', fc=colors[0], ec='0')
        for j, amp in enumerate(A):
            ax.bar(WSP + width*(j+2), Req_cl[j], width, label=labels[j], ec='0', fc = colors[j+1])
        ax.annotate(title , xy=(0.5, 0.97), xycoords='axes fraction',
                size=10, ha='center', va='top',
                bbox=dict(ec='w', fc='w', alpha=0.7))




# labels
    fig.text(0.06, 0.5, 'Equivalent Bending Moment [kNm]', va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'Wind Speed [m/s]', ha='center', rotation='horizontal')
    axes.ravel()[1].legend(ncol=5,bbox_to_anchor=(1.3, 1.2))
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



