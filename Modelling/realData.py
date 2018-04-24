# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:19:41 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime

filename = 'C:\iRotor_Predix_04042018_10pmto11pm_40ms.csv'


def loadData(filename):
    data = []
    with open(filename) as f:
        f.readline()
        for line in f:
            data.append(line)

    # Data processing
    # remove newlines
    data = [line[:-1] for line in data]
    # split data by commas
    data = [line.split(',') for line in data]
    # convert date to datetime object
    t = [0]
    for i, line in enumerate(data):
        datetimeObj = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S.%f')
        if i == 0:
            t0 = datetimeObj
        else:
            t.append((datetimeObj-t0).total_seconds())

    x = [[int(y) for y in line[2:5]] for line in data]
    azim = [float(line[1]) for line in data]
    wsp = [float(line[6]) for line in data]

    return np.array(t), np.array(x), np.array(azim), np.array(wsp)



def hexbinPlot(x, y, ax):
    #extent = [0, 360, min(refy.min(), y.min()), max(refy.max(), y.max())]
    #hexbinConfig = {'gridsize':30, 'extent':extent}
    hexbinConfig = {'gridsize':50, 'linewidths':1}
    ax.hexbin(x, y, cmap='viridis', **hexbinConfig)
    ax.autoscale()


if __name__ == '__main__':
    Fs = 25 # ts = 0.04
    t, x, azim, wsp = loadData(filename)
    xbar = np.mean(x, 1)
    # Calculate spectrum for each blade
    Yave = []
    for b in [0, 1, 2]:
        Ys = []
        f, Py = signal.welch(x[:, b], Fs, nperseg=1024*16)
        Ys.append(np.sqrt(Fs*Py/60000))
        Yave.append(np.mean(Ys, axis=0))

    plt.figure()
    plt.xlim([0, 1])
    for b in [0, 1, 2]:
        plt.plot(f, Yave[b])


    # Hexbin plot
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=[6,6])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)
    for b in [0, 1, 2]:
        hexbinPlot(azim, x[:, b] - xbar, ax[b])





