# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc




def plot_angle_timeseries(dlc, dlc_noipc, c, wsp=26, save=False):
    # get relevant simuation data
    sims = dlc(wsp=wsp, yaw=0, controller=c)
    ref_sim = dlc_noipc(wsp=wsp, yaw=0)
    plt.figure()
    plt.xlabel('Time [s]')
    plt.ylabel('Blade pitch angle [deg]')
    plt.xlim([200,300])

    plt.plot(ref_sim[0].seeds[0].Data.t, ref_sim[0].seeds[0].Data.pitch1, label='no control')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitch1, ls='--', label='Blade 1')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitch2, ls='--', label='Blade 2')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitch3, ls='--', label='Blade 3')

    plt.legend()
    if save:
        plt.savefig('../Figures/{}/{}_pitchangle_{}.png'.format(c, c, wsp), dpi=200)
    plt.show(); print()



def plot_rate_timeseries(dlc, dlc_noipc, c, wsp=26, save=False):
    # get relevant simuation data
    sims = dlc(wsp=wsp, yaw=0, controller=c)
    ref_sim = dlc_noipc(wsp=wsp, yaw=0)
    plt.figure()
    plt.xlabel('Time [s]')
    plt.ylabel('Blade pitch rate [deg]')
    plt.xlim([200,250])

    plt.plot(ref_sim[0].seeds[0].Data.t, ref_sim[0].seeds[0].Data.pitchrate1, label='no control')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate1, ls='--', label='Blade 1')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate2, ls='--', label='Blade 2')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate3, ls='--', label='Blade 3')

    plt.legend()
    if save:
        plt.savefig('../Figures/{}/{}_pitchrate_{}.png'.format(c, c, wsp), dpi=200)
    plt.show(); print()


def plot_histogram(dataIPC, dataRef, c, wsp=26, save=False):
    # get relevant simuation data

    # Pitch rate histogram
    fig, ax = plt.subplots()
    ax.set_xlabel('Blade pitch rate [deg/s]')
    ax.set_ylabel('Frequency')
    ax.set_xlim([-20, 20])
    ax.set_ylim([0, 80000])
    ax.axvline(-10, lw=1, c='k', ls='--')
    ax.axvline(10, lw=1, c='k', ls='--')


    pitchrate = []
    for data in dataRef:
        pitchrate += list(data.pitchrate1)
        pitchrate += list(data.pitchrate2)
        pitchrate += list(data.pitchrate3)

    pitchrateIPC = []
    for data in dataIPC:
        pitchrateIPC += list(data.pitchrate1)
        pitchrateIPC += list(data.pitchrate2)
        pitchrateIPC += list(data.pitchrate3)

    ax.hist(pitchrateIPC, 30, color='k', alpha=0.7, label='With IPC')
    ax.hist(pitchrate, 30, alpha=0.7, label='No IPC')
    ax.set_title('wsp={} m/s'.format(wsp))
    ax.legend()


    if save:
        plt.savefig('../Figures/{}/{}_pitchrate_hist_{}.png'.format(c, c, wsp), dpi=200)
    plt.show(); print()




def run(dlc, dlc_noipc, c, wsp=26, SAVE=None):
    channels = {'pitch1'    :  4,   #pitch angle blade 1 [deg]
                'pitch2'    :  6,
                'pitch3'    :  8,
                'pitchrate1':  5,  # Pitch rate blade 1 [deg/s]
                'pitchrate2':  7,
                'pitchrate3':  9}

    dataRef = [seed.loadFromSel(channels) for seed in dlc_noipc(wsp=wsp)[0]]
    dataIPC = [seed.loadFromSel(channels) for seed in dlc(wsp=wsp,controller=c)[0]]
    plot_histogram(dataIPC, dataRef, c, wsp=wsp, save=SAVE)
    #plot_angle_timeseries(dlc, dlc_noipc, c, wsp=wsp, save=SAVE)
    #plot_rate_timeseries(dlc, dlc_noipc, c, wsp=wsp, save=SAVE)



if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis()

    dlc = PostProc.DLC('dlc11_1')
    dlc.analysis()

    run(dlc, dlc_noipc, 'ipcpi', wsp=26, SAVE=False)