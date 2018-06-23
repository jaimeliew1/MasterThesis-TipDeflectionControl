# -*- coding: utf-8 -*-
"""
Created on Wed June 20 2018

An attempt to perform system identification using only Python
@author: J


"""
import os
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from JaimesThesisModule.Misc import readHawc2Res
from Configuration.Config import Config

plt.rc('text', usetex=True)
dir_res = Config.modelpath + 'res/Pitchstep/'

def loadData(dir_res):
    channels = {
        't'         : 1,    #time [s]
        'TD1'       : 49,   #Tip deflection - blade 1 [m]
        'IPCDem1'   : 99,   #IPC pitch demand - blade 1 [rad]
    }

    # get files with the filename form 'pitchstep_xx' where xx is the wind speed
    # of the simulation.
    resFiles = [x[:-4] for x in os.listdir(dir_res) if x.endswith('.sel')]
    resFiles = [x for x in resFiles if x.startswith('pitchstep_lin')]

    wsps = [int(x.split('_')[2]) for x in resFiles]
    print('Result files found:')
    [print(wsp, x) for wsp, x in zip(wsps, resFiles)]

    # Load results for each windspeed
    resData = []
    for file in resFiles:
        resData.append(readHawc2Res(dir_res + file, channels))

    # extract just the input and output timeseries, and remove first 110 seconds

    PDs = {}
    for data, wsp in zip(resData, wsps):
        PDs[wsp] = pd.DataFrame({'t': data.t,
                                 'x': -data.IPCDem1, # POSSIBLE SOURCE OF SIGN ERROR
                                 'y': data.TD1})

        PDs[wsp] = PDs[wsp][PDs[wsp].t > 110]
        PDs[wsp].t -= 110
        #PDs[wsp].x -= PDs[wsp].x.values[0]
        #PDs[wsp].y -= PDs[wsp].y.mean()

    return PDs



def plot_ts(PDs):
    for wsp, df in PDs.items():
        fig, axes = plt.subplots(2,1, sharex=True)
        plt.subplots_adjust(hspace=0.1)
        axes[0].set_xlim([0, 90])
        axes[0].plot(df.t, df.x)
        axes[1].plot(df.t, df.y)

        fig.suptitle(f'$U = {{{wsp}}}$')
        axes[1].set_xlabel('Time [s]')
        axes[0].set_ylabel('$\~{x}(t) [rad]$')
        axes[1].set_ylabel('$\~{y}(t) [m]$')

        plt.show(); print()


def identify1(X, Y, fs=1, nperseg=500):
        f, Pxy = signal.csd(X, Y, fs=fs, nperseg=nperseg)
        f, Pxx = signal.welch(X, fs=fs, nperseg=nperseg)
        f, pyy = signal.welch(Y, fs=fs, nperseg=nperseg)

        return f, Pxy/Pxx

def identify2(X, Y, fs=1):
        x_f = np.fft.fft(X)
        y_f = np.fft.fft(Y)
        f = np.fft.fftfreq(len(X), 1/fs)
        return f, y_f/x_f


if __name__ == '__main__':

    data = loadData(dir_res)


    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].set_xlim(0.01, 10)
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[1].set_xscale('log')

    for wsp in [18]:#[6, 12, 18, 24]:
        d = data[wsp]


        f2, G2 = identify2(d.x, d.y, fs=100)
        ax[0].plot(f2, abs(G2), '.',  label=f'{wsp}m/s', ms=1)
        ax[1].plot(f2, np.angle(G2, deg=True), '.', ms=1)

        f, G1 = identify1(d.x, d.y, fs=100)
        ax[0].plot(f, abs(G1), label=f'{wsp}m/s')
        ax[1].plot(f, np.angle(G1, deg=True))



    fc = 0.5
    tau = 1/(2*np.pi*fc)
    tf = signal.TransferFunction([43], [tau**2, 2*tau,  1])
    w, H = signal.freqresp(tf, w=f*2*np.pi)
    #ax[0].plot(w/(2*np.pi), abs(H), '--k', label=f'a')
    #ax[1].plot(w/(2*np.pi), np.angle(H, deg=True), '--k')
    ax[0].legend(ncol=2)







