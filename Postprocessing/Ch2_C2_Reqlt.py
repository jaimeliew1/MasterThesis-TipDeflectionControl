# -*- coding: utf-8 -*-
"""
Calculates the lifetime equivalent load for simulation data.
@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
from Other.Weibull import wsp_probs
import math


def run(dlc, dlc_noipc, SAVE=False):

    C = ['ipcpi', 'ipc04', 'ipc07']
    keys = ['RBMf','MBt', 'MBy']
    labels = ['$C_{PI}$', '$C_{f1p}$', '$C_{2}$']
    ticklabels = ['Blade\n(flapwise)', 'Main\nBearing\n (tilt)', 'Main\nBearing\n(yaw)']
    N = len(keys)

    Req_ref, Req_l = np.zeros(len(keys)), np.zeros([len(C), len(keys)])

    for i, key in enumerate(keys):
        Req_ref[i] = lifetimeReq(dlc_noipc.Sims, key)

        for j, c in enumerate(C):
            Req_l[j, i] = lifetimeReq(dlc(controller=c), key)

   # bar graph
    width = 0.8/(len(C) + 1)
    ind = np.arange(N)

    fig, ax = plt.subplots()
    ax.set_ylabel('$R_{eq}$ [kNm]')
    ax.set_xticks(ind + 0.4)
    ax.set_xticklabels(ticklabels)
    ax.bar(ind, Req_ref, width, label = 'No IPC', hatch='\\\\', fc='0.8', ec='0')
    for j, c in enumerate(C):
        ax.bar(ind + width*(j+1), Req_l[j, :], width, label=labels[j], ec='0')

    ax.legend(ncol=2)

    if SAVE:
        pass
        #plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()


    # Save table data
    tableRows = ['Blade (flap)', 'Main Bearing (tilt)', 'Main Bearing (yaw)']
    with open('../Figures/Tables/Ch2_C2_Reqlt.txt', 'w') as f:
        for i in range(3):
            line = tableRows[i] + '&'
            for j in range(3):
                line += '{:2.0f} & {:+2.2f} &'.format(
                        Req_l[j, i], (Req_l[j, i]/Req_ref[i] - 1)*100)
            line = line[:-1] +  '\\\\'
            print(line)
            f.write(line)





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

def fullDatasetGen(dlc):
    # A generator function that yields lists of Simulation objects of a set.
    # Each set has the same controller and gain parameters (yaw = 0),
    # and contains simulations for the full range of windspeeds from 4 to 26 m/s.
    # Additionally, there is no shutdown in any of the simulations.
    wsp_range = range(4, 27, 2)

    param_combs = dlc.unique(['controller', 'Kp'])
    for i, (c, g) in enumerate(param_combs):
        sims_ = dlc(controller=c, Kp=g, yaw=0)

        # skip simulation sets without fill range of wind speeds.
        if not all(x.wsp in wsp_range for x in sims_):
            continue
        # skip simulation sets with shutdown
        if any(x.shutdown for x in sims_):
            continue
        yield sims_

if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')


    run(dlc, dlc_noipc, SAVE=False)







