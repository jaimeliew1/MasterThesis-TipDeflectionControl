# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from JaimesThesisModule import PostProc



def table(X, SAVE=False):
    N = len(X)
    M = 4 # amp, std, min, max
    dat = np.zeros([M, N])


    for i, x in enumerate(X.keys()): #amplitude row
        dat[0, i] = x
    for i, x in enumerate(X.values()): #std row
        dat[1, i] = np.std(x)
    for i, x in enumerate(X.values()): #min row
        dat[2, i] = np.min(x)
    for i, x in enumerate(X.values()): #amplitude row
        dat[3, i] = np.max(x)


    out = '  & \multicolumn{5}{c|}{Reference amplitude [m]}\\\\\n'
    rowtitle = ['std dev','min','max']
    for i, row in enumerate(dat):
        if i == 0:
           out+=  'Pitch rate [$^o/s$]&' + ' & '.join(f'{x:2.0f}' for x in row) + '\\\\\n'
           out += '\\hline \n  '
        else:
            out+= rowtitle[i-1] + '&' + ' & '.join(f'{x:2.2f}' for x in row) + '\\\\\n'
    print(out)
    if SAVE:
        with open('../Figures/Tables/Ch3_Pitchrate.txt', 'w') as f:
            f.write(out)




vp_settings =  {'vert'      :False,
                'showmeans' :True,
                'widths'    :0.3}
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




def get_pr_data_from_sim(sim):
    # Pitch rate of each blade [deg/s]
    channels = {'PR1':  5, 'PR2':  7, 'PR3':  9}
    pr = []
    for seed in sim:
        if seed.data.shutdown:
            continue
        data = seed.loadFromSel(channels=channels)
        for key in channels.keys():
            pr += list(data[key])
    if len(pr) == 0:
        pr = [0]
    return pr





def run(dlcs, SAVE=None):
    if SAVE:
        SAVE1 = SAVE[:-4] + '_normal.png'
        SAVE2 = SAVE[:-4] + '_inverse.png'
    else:
        SAVE1 = SAVE2 = None
    _run(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'], SAVE=SAVE1)
    _run(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'], SAVE=SAVE2)



def _run(dlc_noipc, dlc1, dlc2, wsp=18, SAVE=None):
    labels = ['no\nIPC', '$0m$', '$1m$', '$2m$', '$3m$']

    pr_noipc = get_pr_data_from_sim(dlc_noipc(wsp=wsp)[0])

    # ipc04 tower clearances
    c = 'ipc04'
    pr1 = {0:get_pr_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
    for a in [1, 2, 3]:
        pr1[a] = get_pr_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])

    # ipc04 tower clearances
    c = 'ipc07'
    pr2 = {0:get_pr_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
    for a in [1, 2, 3]:
        pr2[a] = get_pr_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])


    # plot setup
    plt.figure(figsize=[4, 4])
    #plt.xlim(7, 24)
    plt.axvline(-10, lw=1, c='k', ls='--')
    plt.axvline(10, lw=1, c='k', ls='--')
    plt.yticks(np.arange(5), labels)
    plt.xlabel('Blade Pitch Rate $[^o/s]$')
    plt.ylabel('Tip Tracking Amplitude $[m]$')


    parts = plt.violinplot([pr_noipc], positions=[0], **vp_settings)
    formatViolinplot(parts, color = 'tab:orange')

    positions = np.array([1, 2, 3, 4]) - 0.1
    parts = plt.violinplot(pr1.values(), positions=positions, **vp_settings)
    formatViolinplot(parts, colors[0])

    positions = np.array([1, 2, 3, 4]) + 0.1
    parts = plt.violinplot(pr2.values(), positions=positions, **vp_settings)
    formatViolinplot(parts, colors[-1])

    # make proxy object for legend as violinplots do not support legends.
    a1 = mpatches.Patch(fc='tab:orange', ec='k', alpha=0.7, label='No IPC')
    a2 = mpatches.Patch(fc=colors[0], ec='k', alpha=0.7, label='$C_{f1p}$')
    a3 = mpatches.Patch(fc=colors[-1], ec='k', alpha=0.7, label='$C_{2}$')
    plt.legend(handles = [a1, a2, a3], ncol=3, bbox_to_anchor=(0.98, 1.15))

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()


    #table(X, SAVE)
    return X







if __name__ is '__main__':
    dlcs = {'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}


    X = run(dlcs, SAVE=False)












