# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
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




def formatViolinplot(parts, colors=None):

    for i, pc in enumerate(parts['bodies']):
        if colors:
            pc.set_facecolor(colors[i])
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    for key in ['cbars', 'cmins', 'cmaxes', 'cmeans']:
        parts[key].set_color('black')
        parts[key].set_linewidth(1)




def run(dlcs, wsp=18, c='ipc07', maxAmp=3, SAVE=False):
    dlc_noipc = dlcs['dlc11_0']
    dlc = dlcs['dlc11_1']
    dlc2 = dlcs['dlc11_3']
    channels = {'PR1':  5,  # Pitch rate blade 1 [deg/s]
                'PR2':  7,
                'PR3':  9}

    #%% Load pitch rate of all blades into dictionary of lists
    X = {}
    labels = ['no\nIPC'] + [f'${x}m$' for x in range(maxAmp+1)]

    # load data for no IPC
    Sims = dlc_noipc(wsp=wsp)[0]
    X['noipc'] = []
    for seed in Sims:
        data = seed.loadFromSel(channels=channels)
        for key in channels.keys():
            X['noipc'] += list(data[key])


    # Load data for 0m tracking
    Sims = dlc(wsp=wsp, controller=c)[0]
    X[0] = []
    for seed in Sims:
        data = seed.loadFromSel(channels=channels)
        for key in channels.keys():
            X[0] += list(data[key])


    # Load data for TTT where amp = 1, 2, 3
    for a in range(1, maxAmp+1):
        Sims = dlc2(wsp=wsp, controller=c, _amp=a)[0]
        X[a] = []
        for seed in Sims:
            data = seed.loadFromSel(channels=channels)
            for key in channels.keys():
                X[a] += list(data[key])




    plt.figure(figsize=[4, 4])
    plt.xlim(-12, 12)
    plt.axvline(x=-10, lw=1, ls='--', c='k')
    plt.axvline(x=10, lw=1, ls='--', c='k')
    plt.xlabel('Blade pitch rate $[^o/s]$')
    plt.ylabel('Tip Tracking Amplitude')
    parts = plt.violinplot(X.values(), positions=np.arange(len(X)), vert=False, showmeans=True)
    # http://colorbrewer2.org
    colors = ['0.7', '#ffffcc','#a1dab4','#41b6c4','#2c7fb8','#253494']
    formatViolinplot(parts, colors)

    plt.yticks(np.arange(len(X)), labels)


    if SAVE:
        plt.savefig(SAVE, dpi=300, bbox_inches='tight')
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


    X = run(dlcs, wsp=18, c='ipc07', maxAmp=4, SAVE=False)
    #run(PostProc.DLC('dlc15_0'), PostProc.DLC('dlc15_1'), PostProc.DLC('dlc15_2'), wsp=18, c='ipc04', maxAmp=4, SAVE=False)

    #%%











