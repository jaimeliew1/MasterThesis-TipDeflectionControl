# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from JaimesThesisModule import PostProc
from scipy.stats import gaussian_kde


def kde_scipy(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    # Note that scipy weights its bandwidth by the covariance of the
    # input data.  To make the results comparable to the other methods,
    # we divide the bandwidth by the sample standard deviation here.
    #kde = gaussian_kde(x, bw_method=bandwidth / np.std(x, ddof=1), **kwargs)
    kde = gaussian_kde(x, bw_method=bandwidth, **kwargs)
    return kde.evaluate(x_grid)





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





# http://colorbrewer2.org/
colors = ['#ffffcc','#a1dab4','#41b6c4','#225ea8']





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
    labels = ['no\nIPC', '$0m$', '$1m$', '$2m$', '$3m$', '$4m$']

    pr_noipc = get_pr_data_from_sim(dlc_noipc(wsp=wsp)[0])

    # ipc04 tower clearances
#    c = 'ipc04'
#    pr1 = {0:get_pr_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
#    for a in [1, 2, 3, 4]:
#        pr1[a] = get_pr_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])

    # ipc07 pitch rate
    c = 'ipc07'
    pr2 = {0:get_pr_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
    for a in [1, 2, 3, 4]:
        pr2[a] = get_pr_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])


    cmap = mpl.cm.get_cmap('Blues')
    fig, ax = plt.subplots()
    x_ = np.linspace(-15, 15, 100)
    plt.axvline(-10, ls='--', c='k', lw=1)
    plt.axvline(10, ls='--', c='k', lw=1)
    kde = kde_scipy(pr_noipc, x_, bandwidth=0.15)
    plt.plot(x_, kde, '--', color='tab:orange', label='no IPC')

    for i, x in enumerate(pr2.values()):
        label = f'{i}m tracking'
        c = cmap((i+2)/6)
        kde = kde_scipy(x, x_, bandwidth=0.10)
        plt.plot(x_, kde, color=c, label=label)




    # labels
    ax.set_xlabel('Blade Pitch Rate $[^o/s]$')
    ax.set_ylabel('Probability [-]')

    # ticks
    start, stop = ax.get_xlim()
    ax.set_xticks(range(int(start), int(stop)+1, 1), minor=True)
    #ax.set_yticks(np.arange(0, 0.21, 0.1))
    ax.set_ylim(0, 0.3)
    ax.legend()

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()


    #table(X, SAVE)








if __name__ is '__main__':
    dlcs = {'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}


    run(dlcs, SAVE=False)












