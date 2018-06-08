# -*- coding: utf-8 -*-
"""
A module which performs analysis on a certain aspect of the tip deflection
controller results.

This script analyses: Power Output

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
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
        x += list(data['Pelec'].values)
    return x



def run(dlc, dlc_noipc, c, SAVE=None):

    WSP = np.arange(4, 27, 2)
    X = {}

    for wsp in WSP:
        sim = dlc_noipc(wsp=wsp)[0]
        X[wsp] = get_pelec_data_from_sim(sim)

    # control case
    X1 = {}
    for wsp in WSP:
        sim = dlc(wsp=wsp, controller=c)[0]
        X1[wsp] = get_pelec_data_from_sim(sim)


    plt.figure(figsize=[7,5])
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('$P_{elec}$ [W]')
    dx = 0.3
    parts = plt.violinplot(X.values(), positions=np.array(list(X.keys())) - dx, **vp_settings)
    formatViolinplot(parts, colors[1])

    parts = plt.violinplot(X1.values(), positions=np.array(list(X1.keys())) + dx, **vp_settings)
    formatViolinplot(parts, colors[-1])


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()

    return X


if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    X = run(dlc, dlc_noipc, 'ipc04', SAVE=False)