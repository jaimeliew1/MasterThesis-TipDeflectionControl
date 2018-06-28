# -*- coding: utf-8 -*-
"""
A module which performs analysis on a certain aspect of the tip deflection
controller results.

This script analyses: Power Output

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from JaimesThesisModule import PostProc



vp_settings =  {'vert'      :True,
                'showmeans' :True,
                'widths'    :1}
# http://colorbrewer2.org/
colors = ['#ffffcc','#a1dab4','#41b6c4','#225ea8']
def formatViolinplot(parts, color=None):

    for i, pc in enumerate(parts['bodies']):
        if color:
            pc.set_facecolor(color)
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    for key in ['cbars', 'cmins', 'cmaxes', 'cmeans']:
        parts[key].set_color('black')
        parts[key].set_linewidth(1)




def get_pelec_data_from_sim(sim):
    x = []
    for seed in sim:
        data = seed.loadFromSel(channels={'Pelec':103})
        x += list(data['Pelec'].values/1e6)
    return x




def run(dlc, dlc_noipc, SAVE=None):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_below_rated.png'
        SAVE2 = SAVE[:-4] + '_above_rated.png'
    else:
        SAVE1 = SAVE2 = None
    _run(dlc, dlc_noipc, WSP = [4, 6, 8, 10, 12, 14], SAVE=SAVE1)
    _run(dlc, dlc_noipc, WSP = [ 16, 18, 20, 22, 24, 26], SAVE=SAVE2)



def _run(dlc, dlc_noipc, WSP= np.arange(4, 27, 2), c='ipc07', SAVE=None):

    #WSP = np.arange(4, 27, 2)
    X = {}

    for wsp in WSP:
        sim = dlc_noipc(wsp=wsp)[0]
        X[wsp] = get_pelec_data_from_sim(sim)

    # control case
    X1 = {}
    for wsp in WSP:
        sim = dlc(wsp=wsp, controller=c)[0]
        X1[wsp] = get_pelec_data_from_sim(sim)


    plt.figure(figsize=[4,4])
    plt.xticks(WSP)
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Electrical Power Output [MW]')
    dx = 0.3
    parts = plt.violinplot(X.values(), positions=np.array(list(X.keys())) - dx, **vp_settings)
    formatViolinplot(parts, colors[1])

    parts = plt.violinplot(X1.values(), positions=np.array(list(X1.keys())) + dx, **vp_settings)
    formatViolinplot(parts, colors[-1])

    a1 = mpatches.Patch(fc=colors[1], ec='k', alpha=0.7, label='No IPC')
    a2 = mpatches.Patch(fc=colors[-1], ec='k', alpha=0.7, label='IPC ($C_{2}$)')

    plt.legend(handles = [a1, a2], loc='upper left')
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()


#    # print LaTeX table
#    for wsp in WSP:
#        print(f'\multirow{{2}}{{*}} {{{wsp}}} & No IPC &{np.mean(X[wsp]):2.3f} &  {np.std(X[wsp]):2.3f} \\\\')
#        print(f'& IPC ($C_2$) & {np.mean(X1[wsp]):2.3f} &  {np.std(X1[wsp]):2.3f} \\\\ \\hline')
    #return X, X1


if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    run(dlc, dlc_noipc, SAVE=False)