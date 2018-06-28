# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
import math
from Other.Weibull import wsp_probs


def lifetimeReq(sims_, key='RBM'):
    #wohler = Config.Config.wohler[key]
    wohler = {'RBMf':10, 'RBMe':10, 'RBMt':10, 'MBt':4, 'MBy':4}
    # Probability of each wind speed occuring
    P = wsp_probs()
    Y = 0
    for sim in sims_:
        wsp = sim.wsp
        Y += float(sim.data[key]**wohler[key]*P[wsp])

    Req_l = Y**(1/wohler[key])

    return Req_l






def run(dlc, dlc_noipc, SAVE=False):
    dlc2 = PostProc.DLC('dlc11_2')
    _run(dlc, dlc2, dlc_noipc, 'ipcpi', 'ipc_rbmpi', SAVE=SAVE)
    _run(dlc, dlc2, dlc_noipc, 'ipc04', 'ipc_rbm04', SAVE=SAVE)
    _run(dlc, dlc2, dlc_noipc, 'ipc07', 'ipc_rbm07', SAVE=SAVE)


    # Lifetime equivalent load table for ipc07
    keys = ['RBMf', 'MBt', 'MBy']
    tableRows = ['Blade (flap)', 'Main Bearing (tilt)', 'Main Bearing (yaw)']
    f = open('../Figures/Tables/Ch2_RBM_Reqlt.txt', 'w')
    for i, row in enumerate(keys):
        leqref = lifetimeReq(dlc_noipc.Sims, row)
        leq1 = lifetimeReq(dlc(controller='ipc07'), row)
        leq2 = lifetimeReq(dlc2(controller='ipc_rbm07'), row)

        line = tableRows[i]
        line += '& {:2.0f} & {:+2.2f}'.format(
                        leq1, (leq1/leqref - 1)*100)
        line += '& {:2.0f} & {:+2.2f} \\\\\n'.format(
                        leq2, (leq2/leqref - 1)*100)
        f.write(line)
    f.close()


def _run(dlc, dlc2, dlc_noipc, C, C2, SAVE=False):

    #C, C2 = 'ipcpi', 'ipc_rbmpi'

    keys = ['RBMf', 'MBt', 'MBy']
    titles = ['Blade (flapwise)', 'Main bearing (tilt)', 'Main bearing (yaw)']

    #WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
    WSP = np.arange(4, 27, 4)
    fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=[10,3])
    plt.subplots_adjust(wspace=0.05)
    # for eack key and title, make a new bar graph.
    for key, title, ax in zip(keys, titles, axes.ravel()):
        Req_ol, Req, Req2 = [0]*len(WSP), [0]*len(WSP), [0]*len(WSP)

        for i, wsp in enumerate(WSP):
            sim_ref = dlc_noipc(wsp=wsp)[0]
            Req_ol[i] = float(sim_ref.data[key])

            sim = dlc(wsp=wsp, controller=C)[0]
            Req[i] = float(sim.data[key])

            sim = dlc2(wsp=wsp, controller=C2)[0]
            Req2[i] = float(sim.data[key])

       # bar graph
        width = 1


        ax.set_xticks(WSP + 1)
        ax.set_xticklabels(WSP)
        ax.grid(True, axis='y')
        ax.set_axisbelow(True)
        ax.bar(WSP, Req_ol, width, label = 'No IPC', hatch='\\\\', fc='0.8', ec='0')
        ax.bar(WSP + width, Req, width, label='Tip Deflection Sensors', ec='0')
        ax.bar(WSP + 2*width, Req2, width, label='Strain Gauge Sensors', ec='0')
        ax.annotate(title , xy=(0.5, 0.97), xycoords='axes fraction',
                size=10, ha='center', va='top',
                bbox=dict(ec='w', fc='w', alpha=0.7))




# labels
    fig.text(0.06, 0.5, 'Equivalent Bending Moment [kNm]', va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'Wind Speed [m/s]', ha='center', rotation='horizontal')
    axes.ravel()[1].legend(ncol=4,bbox_to_anchor=(1.3, 1.2))
    if SAVE:
        plt.savefig(SAVE[:-4]+C+'.png', dpi=200, bbox_inches='tight')
    plt.show(); print()




if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    run(dlc, dlc_noipc, SAVE=False)



