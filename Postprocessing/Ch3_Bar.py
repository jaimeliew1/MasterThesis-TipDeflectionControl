# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc_noipc, dlc, dlc2, SAVE=False):
    c = 'ipc07'
    key = 'RBMf'
    amps = [1, 2, 3, 4]
    WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])

    # for eack key and title, make a new bar graph.

    Req_ol, Req_cl = [0]*12, np.zeros([len(amps), 12])

    for i, wsp in enumerate(WSP):
        sim_ref = dlc(wsp=wsp, controller=c)[0]
        Req_ol[i] = float(sim_ref.data[key])

        for j, amp in enumerate(amps):
            sim = dlc2(wsp=wsp, _amp=amp, controller=c)[0]
            Req_cl[j, i] = float(sim.data[key])

   # bar graph
    width = 1.4/(len(amps) + 1)

    fig, ax = plt.subplots()
    ax.set_ylabel('$R_{eq}$ [kNm]')
    ax.set_xlabel('Wind Speed [m/s]')
    ax.set_xticks(np.arange(4, 27, 2))
    ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0')
    for j, amp in enumerate(amps):
        ax.bar(WSP + width*(j+1), Req_cl[j], width, label=amp, ec='0')
    ax.set_title('asdf')
    ax.legend()

    plt.show(); print()

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')






if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')
    dlc2 = PostProc.DLC('dlc11_3')

    run(dlc_noipc, dlc, dlc2, SAVE=False)





