# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from JaimesThesisModule import PostProc


def plot(X, SAVE=False):
#%% Plot histogram of closest tower passes.
    histProps = {'bins'     : 30,
                 'alpha'    : 0.7,
                 'normed'   : True,
                 'histtype' : 'stepfilled',
                 'edgecolor': 'k'}

    cmap = mpl.cm.get_cmap('Blues')

    fig, ax = plt.subplots()
    keys = list(X.keys())
    keys.reverse()
    for i, key in enumerate(keys):
        label = f'{i}m tracking'
        c = cmap(key/(len(X)-1))
        ax.hist(X[key], **histProps, facecolor=c, label=label)
    # labels
    ax.set_xlabel('Minimum Passing Blade-Tower Clearance [m]')
    ax.set_ylabel('Probability [-]')

    # ticks
    start, stop = ax.get_xlim()
    ax.set_xticks(range(int(start), int(stop)+1, 1), minor=True)
    ax.set_yticks(np.arange(0, 0.41, 0.1))
    ax.legend()

    if SAVE:
        plt.savefig(SAVE, dpi=300, bbox_inches='tight')
    plt.show(); print()




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
    with open('../Figures/Tables/Ch3_Pitchrate.txt', 'w') as f:
        f.write(out)




def run(dlc_noipc, dlc, dlc2, wsp=18, c='ipc04', maxAmp=3, SAVE=False):
    channels = {'PR1':  5,  # Pitch rate blade 1 [deg/s]
                'PR2':  7,
                'PR3':  9}
    keys = channels.keys()

    #%% Load data into list of x
    X = {}

    # Load data for no TTT
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

    #plot(X, SAVE)
    table(X, SAVE)
    return X








if __name__ is '__main__':
    dlc = PostProc.DLC('dlc11_1')
    dlc2 = PostProc.DLC('dlc11_3')


    X = run(_, dlc, dlc2, wsp=18, c='ipc04', maxAmp=4, SAVE=False)





