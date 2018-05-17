# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def run(dlc_noipc, dlc, dlc2, SAVE=False):

    if SAVE:
        pass
        #plt.savefig('../Figures/{}/.png', dpi=200)





if __name__ is '__main__':
    pass


    #run(dlc_noipc, dlc, dlc2, SAVE=False)



#%%
def binCyclicalData(T, Y, width=1):

    X = np.arange(0, 360, width)
    dat = {k:[] for k in X}
    for t, y in zip(T, Y):
        Bin = 0
        if t%360 != 0:
            Bin =X[X<t%360][-1]
        dat[Bin].append(y)

    #Mean = [np.mean(v) for v in dat.values()]
    #Max = [np.max(v) for v in dat.values()]
    #Min = [np.min(v) for v in dat.values()]

    return dat


#%% Load data into list of x and list of y.
X, Y = [], []
channels = {'Azim': 2, 'TD1': 49, 'TD2' : 52, 'TD3': 55}
wsp=18; key='TD1'; ylabel='Tip Deflection [m]'; c = 'ipc07'
dlc = PostProc.DLC('dlc11_1')
dlc2 = PostProc.DLC('dlc11_3')

# Load data for no TTT
Sims = dlc(wsp=wsp, controller=c)[0]
X.append([]); Y.append([])
for seed in Sims:
    data = seed.loadFromSel(channels)
    X[-1] += list(data.Azim)
    Y[-1] += list(data[key])

# Load data for TTT where amp = 1, 2, 3
for a in [1, 2, 3]:
    Sims = dlc2(wsp=wsp, controller=c, _amp=a)[0]
    X.append([]); Y.append([])
    for seed in Sims:
        data = seed.loadFromSel(channels)
        X[-1] += list(data.Azim)
        Y[-1] += list(data[key])


#%% Plot the statistical data.

def TTTplot(ax, X, Y):
    extent = [0, 360, -10, 10]
    hexbinConfig = {'gridsize':30, 'extent':extent, 'linewidths':1, 'mincnt':1}
    ax.set_ylim(-10, 10)
    hist = binCyclicalData(X, Y)
    bins = list(hist.keys())
    Max = [np.max(v) for v in hist.values()]
    Min = [np.min(v) for v in hist.values()]

    Hexplot = ax.hexbin(X, Y, cmap='Blues', **hexbinConfig)
    ax.plot(bins, Max, '--k')
    ax.plot(bins, Min, '--k')
    ax.set_xticks(range(0, 361, 90))
    ax.set_yticks(range(-8, 9, 4))
    ax.grid()

    return Hexplot # for the color bar








fig, axes = plt.subplots(4, 1, sharex=True, figsize=(6, 7))
plt.subplots_adjust(hspace=0.1)
for i, ax in enumerate(axes):
    hexPlot = TTTplot(ax, X[i], Y[i])

# labels
fig.text(0.04, 0.5, 'Flapwise Tip Deflection (blade FOR) [m]', va='center', rotation='vertical')
axes[-1].set_xlabel('Azimuth Angle [deg]')
# color bar
cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist())
cb.set_label('Number of Occurences')
plt.show(); print()

