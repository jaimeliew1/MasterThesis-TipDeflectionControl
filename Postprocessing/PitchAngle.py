# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc, ref_dlc=None, save=None):

    # Pitch angle vs time
    wsp, k = 26, -1
    controllers = dlc.unique(['controller'])
    controllers = ['ipc04']
    plt.figure()
    plt.title('wsp: {}, Kp: {:2.0f}mrad/m'.format(wsp, -k*1000))
    ref_sim = ref_dlc(wsp=wsp, yaw=0)
    plt.plot(ref_sim[0].seeds[0].Data.t, ref_sim[0].seeds[0].Data.pitch1, label='no control')
    for c in controllers:
        sims = dlc(wsp = wsp, yaw=0, controller=c, Kp=k)
        plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitch1, ls='--', label=c[0])

    plt.legend()
    plt.xlim([200,300])

    plt.xlabel('Time [s]')
    plt.ylabel('Blade 1 pitch angle [deg]')

    #Pitch rate vs time
    plt.figure()
    ref_sim = ref_dlc(wsp=wsp, yaw=0)
    plt.plot(ref_sim[0].seeds[0].Data.t, ref_sim[0].seeds[0].Data.pitchrate1, label='no control')
    for c in controllers:
        sims = dlc(wsp = wsp, yaw=0, controller=c, Kp=k)
        plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate1, ls='--', label=c[0])

    plt.axhline(y=10, c='k', lw=1, ls='--')
    plt.axhline(y=-10, c='k', lw=1, ls='--')
    plt.legend()

    plt.xlabel('Time [s]')
    plt.ylabel('Blade 1 pitch rate [deg/s]')
    plt.show()

def plot_angle_timeseries(dlc, dlc_noipc, wsp, c, save=False):
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
        plt.savefig('../Figures/Pitchrate/pitchangle_{}_{}.png'.format(c, wsp), dpi=200)



def plot_rate_timeseries(dlc, dlc_noipc, wsp, c, save=False):
    # get relevant simuation data
    sims = dlc(wsp=wsp, yaw=0, controller=c)
    ref_sim = dlc_noipc(wsp=wsp, yaw=0)
    plt.figure()
    plt.xlabel('Time [s]')
    plt.ylabel('Blade rate angle [deg]')
    plt.xlim([200,250])

    plt.plot(ref_sim[0].seeds[0].Data.t, ref_sim[0].seeds[0].Data.pitchrate1, label='no control')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate1, ls='--', label='Blade 1')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate2, ls='--', label='Blade 2')
    plt.plot(sims[0].seeds[0].Data.t, sims[0].seeds[0].Data.pitchrate3, ls='--', label='Blade 3')

    plt.legend()
    if save:
        plt.savefig('../Figures/Pitchrate/pitchrate_{}_{}.png'.format(c, wsp), dpi=200)


def plot_histogram(dlc, dlc_noipc, wsp, c, save=False):
    # get relevant simuation data
    sims = dlc(wsp=wsp, yaw=0, controller=c)
    ref_sims = dlc_noipc(wsp=wsp, yaw=0)
    # Pitch rate histogram
    fig, ax = plt.subplots()
    ax.set_xlabel('Blade pitch rate [deg]')
    ax.set_ylabel('Frequency')
    ax.set_xlim([-20, 20])
    ax.set_ylim([0, 8000])
    ax.axvline(-10, lw=1, c='k', ls='--')
    ax.axvline(10, lw=1, c='k', ls='--')



    ax.hist(sims[0][0].Data.pitchrate1, 30, alpha=0.7, label=c)
    ax.hist(ref_sims[0][0].Data.pitchrate1, 30, color='k', alpha=0.7, label='No Control')

    ax.legend()
    plt.show(); print()

    if save:
        plt.savefig('../Figures/Pitchrate/pitchrate_hist_{}_{}.png'.format(c, wsp), dpi=200)




def run(dlc, dlc_noipc, wsp, c, save=None):
    plot_histogram(dlc, dlc_noipc, wsp, c, save=save)
    plot_angle_timeseries(dlc, dlc_noipc, wsp, c, save=save)
    plot_rate_timeseries(dlc, dlc_noipc, wsp, c, save=save)
if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc, 12, 'ipc04', save=True)