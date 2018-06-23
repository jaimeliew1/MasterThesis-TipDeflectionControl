# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
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



def run(dlcs, SAVE=None):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_normal.png'
        SAVE4 = SAVE[:-4] + '_inverse.png'
    else:
        SAVE1 = SAVE4= None
    _run(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'], SAVE=SAVE1)
    _run(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'],SAVE=SAVE4)


def plot_bars_on_ax(ax, dlc_noipc, dlc, dlc2, c, key):
    A = [1, 2, 3, 4]
    WSP = np.arange(4, 27, 4)
    labels = ['$A_r=1$', '$A_r=2$', '$A_r=3$', '$A_r=4$']
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
    #colors = ['#ffffcc','#a1dab4','#41b6c4','#225ea8']
    colors = ['#ffffcc','#a1dab4','#41b6c4','#2c7fb8','#253494']

    ax.bar(WSP, Req_ol, width, label = 'No control', hatch='\\\\', fc='0.8', ec='0')
    ax.bar(WSP + width, Req_0, width, label = '$A_r=0$', fc=colors[0], ec='0')
    for j, amp in enumerate(A):
        ax.bar(WSP + width*(j+2), Req_cl[j], width, label=labels[j], ec='0', fc = colors[j+1])







def _run(dlc_noipc, dlc, dlc2, SAVE=False):
    keys = ['RBMf', 'MBt', 'MBy']
    titles = ['Blade (flapwise)',
              'Main bearing (tilt)', 'Main bearing (yaw)']

    WSP = np.arange(4, 27, 4)
    fig, axes = plt.subplots(2, 3, sharex=True, sharey=True, figsize=[10,5])
    plt.subplots_adjust(wspace=0.05, hspace=0.07)
    for ax in axes.ravel():
        ax.set_xticks(WSP + 1)
        ax.set_xticklabels(WSP)
        ax.grid(True, axis='y')
        ax.set_axisbelow(True)
        ax.set_ylim(0, 30000)

    # ipc04
    for key, title, ax in zip(keys, titles, axes[0, :]):
        plot_bars_on_ax(ax, dlc_noipc, dlc, dlc2, 'ipc04', key)
        ax.annotate(title , xy=(0.5, 0.97), xycoords='axes fraction',
                size=10, ha='center', va='top',
                bbox=dict(ec='w', fc='w', alpha=0.0))

    # ipc07
    for key, title, ax in zip(keys, titles, axes[1, :]):
        plot_bars_on_ax(ax, dlc_noipc, dlc, dlc2, 'ipc07', key)
        ax.annotate(title , xy=(0.5, 0.95), xycoords='axes fraction',
                size=10, ha='center', va='top',
                bbox=dict(ec='w', fc='w', alpha=0.0))

# labels
    fig.text(0.06, 0.5, 'Equivalent Bending Moment [kNm]', va='center', rotation='vertical')
    fig.text(0.5, 0.05, 'Wind Speed [m/s]', ha='center', rotation='horizontal')
    axes.ravel()[1].legend(ncol=6,bbox_to_anchor=(1.8, 1.3))
    axes[0, -1].text(1.01, 0.5, '$C_{f1p}$', size=12, rotation=-90,  transform=axes[0, -1].transAxes)
    axes[1, -1].text(1.01, 0.5, '$C_{2}$', size=12, rotation=-90,  transform=axes[1, -1].transAxes)
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()



    # lifetime equivalent load table

    tableRows = ['Blade (flap)', 'Main Bearing (tilt)', 'Main Bearing (yaw)']
    #f = open('../Figures/Tables/Ch3_extreme_Reqlt.txt', 'w')
    C = 'ipc07'
    for i, row in enumerate(keys):
        leqref = lifetimeReq(dlc_noipc.Sims, row)
        leq0 = lifetimeReq(dlc(controller=C), row)
        line = tableRows[i]
        line += '& {:2.0f} & {:+2.2f}'.format(
                        leq0, (leq0/leqref - 1)*100)
        for amp in [1, 2, 3, 4]:
            leq1 = lifetimeReq(dlc2(controller=C, _amp=amp), row)


            line += '& {:2.0f} & {:+2.2f}'.format(
                        leq1, (leq1/leqref - 1)*100)

        #f.write(line)
        print(line)
    #f.close()




if __name__ is '__main__':
    dlcs = {
    'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}
    run(dlcs, SAVE=False)



