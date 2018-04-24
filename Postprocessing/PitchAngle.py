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


def plot_histogram(dlc, dlc_noipc, c, wsp=26, save=False):
    # get relevant simuation data
    sims = dlc(wsp=wsp, yaw=0, controller=c)
    ref_sims = dlc_noipc(wsp=wsp, yaw=0)
    # Pitch rate histogram
    fig, ax = plt.subplots()
    ax.set_xlabel('Blade pitch rate [deg/s]')
    ax.set_ylabel('Frequency')
    ax.set_xlim([-20, 20])
    ax.set_ylim([0, 8000])
    ax.axvline(-10, lw=1, c='k', ls='--')
    ax.axvline(10, lw=1, c='k', ls='--')



    ax.hist(sims[0][0].Data.pitchrate1, 30, alpha=0.7, label='With IPC')
    ax.hist(ref_sims[0][0].Data.pitchrate1, 30, color='k', alpha=0.7, label='No IPC')
    ax.set_title('wsp={} m/s'.format(wsp))
    ax.legend()


    if save:
        plt.savefig('../Figures/{}/{}_pitchrate_hist_{}.png'.format(c, c, wsp), dpi=200)
    plt.show(); print()




def run(dlc, dlc_noipc, c, wsp=26, SAVE=None):
    plot_histogram(dlc, dlc_noipc, c, wsp=wsp, save=SAVE)
    plot_angle_timeseries(dlc, dlc_noipc, c, wsp=wsp, save=SAVE)
    plot_rate_timeseries(dlc, dlc_noipc, c, wsp=wsp, save=SAVE)



if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc, 'ipc04', wsp=26, SAVE=True)