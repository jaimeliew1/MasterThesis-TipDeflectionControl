# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc




def plotShutdown(seed, SAVE=None):
    channels={'status': 91, 't':1, 'p1': 4 ,'p2': 6, 'p3': 8, 'PPDem': 71}
    data = seed.loadFromSel(channels=channels)
    t = data.t
    x = [(data.p1 - np.rad2deg(data.PPDem)).values,
         (data.p2 - np.rad2deg(data.PPDem)).values,
         (data.p3 - np.rad2deg(data.PPDem)).values]


    N = 500 # running average box length (5 seconds @ 100Hz)
    t_sd = data.t.values[data.status>0][0] # shutdown time
    if t_sd < 105:
        return
    x_ave = [np.convolve(x_, np.ones((N,))/N, mode='same') for x_ in x]

    plt.figure()
    plt.xlabel('Time [s]')
    plt.ylabel('Time averaged pitch angle deviation [$^o$]')


    dt = 100
    plt.xlim(t_sd - dt, t_sd + 5)
    plt.ylim(-3, 3)
    for x_ in x_ave:
        plt.plot(t[t<t_sd], x_[t<t_sd])

    plt.axvline(t_sd, lw=2, ls='-', c='k')
    plt.axhline(2, lw=1, ls='--', c='r')
    plt.axhline(-2, lw=1, ls='--', c='r')
    plt.text(t_sd, 0, 'Turbine Shutdown', rotation=-90, va='center')
    plt.text(t_sd - dt/2, 2.05, 'Threshold', ha='center')
    plt.legend(['1', '2', '3'], loc='center left', title='Blade')

    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()




def run(dlc, dlc_noipc, SAVE=False):
    dlc = PostProc.DLC('dlc13_1')
    shutdownseeds = []
    for seed in dlc.seeds:
        if seed.data.shutdown:
            data = seed.loadFromSel(channels={'status': 91})
            print(seed, '\tshutdown status:', data.status.values[-1])
            shutdownseeds.append(seed)

    plotShutdown(shutdownseeds[8], SAVE)




if __name__ is '__main__':

    run(0, 0, SAVE=False)



