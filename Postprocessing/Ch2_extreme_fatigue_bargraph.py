# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
import math



def wsp_probs(Class=1, dx=2, Range= [4, 26.1]):
    # Weibull Parameters
    k = 2
    if Class == 1:
        A = 10/math.gamma(1+1/k)
    elif Class == 2:
        A = 8.5/math.gamma(1+1/k)
    elif Class == 3:
        A = 7.5/math.gamma(1+1/k)

    # Weibull cdf function
    cdf = lambda x: 1 - np.exp(-(x/A)**k)
    #Discrete wind speeds
    Y = np.arange(Range[0], Range[1], dx)

    # Probabilities of each wind speed
    P = [cdf(y+dx/2) - cdf(y-dx/2) for y in Y]

    return dict(zip(Y, P))

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

    C = ['ipc04', 'ipc07']
    keys = ['RBMf', 'MBt', 'MBy']
    titles = ['Blade (flapwise)',
              'Main bearing (tilt)', 'Main bearing (yaw)']
    labels = ['$C_{PI}$', '$C_{f1p}$', '$C_{2}$']
    #WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
    WSP = np.arange(4, 27, 4)
    fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=[10,3])
    plt.subplots_adjust(wspace=0.05)
    # for eack key and title, make a new bar graph.
    for key, title, ax in zip(keys, titles, axes.ravel()):
        Req_ol, Req_cl = [0]*len(WSP), np.zeros([len(C), len(WSP)])

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


    # lifetime equivalent load table

    tableRows = ['Blade (flap)', 'Main Bearing (tilt)', 'Main Bearing (yaw)']
    f = open('../Figures/Tables/Ch2_extreme_Reqlt.txt', 'w')
    for i, row in enumerate(keys):
        leqref = lifetimeReq(dlc_noipc.Sims, row)
        leq1 = lifetimeReq(dlc(controller='ipc04'), row)
        leq2 = lifetimeReq(dlc(controller='ipc07'), row)

        line = tableRows[i]
        line += '& {:2.0f} & {:+2.2f}'.format(
                        leq1, (leq1/leqref - 1)*100)
        line += '& {:2.0f} & {:+2.2f} \\\\\n'.format(
                        leq2, (leq2/leqref - 1)*100)
        f.write(line)
        print(line)
    f.close()




if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc13_0')
    dlc = PostProc.DLC('dlc13_1')

    run(dlc, dlc_noipc, SAVE=False)



