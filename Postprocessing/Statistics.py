# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:30:25 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc, ref_dlc=None, save=None, key='MBy', unit='kNm'):
    #key = 'RBM1'; unit = 'kNm'
    #key = 'MBy'; unit = 'kNm'
    #key = 'MTBy'; unit = 'kNm'
    #key = 'TD1'; unit = 'm'
    #key = 'Pelec'; unit = 'W'
    plt.figure()
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('{} [{}]'.format(key, unit))
    plt.grid()
    plt.autoscale(axis='y',tight=True)
    wsp_ = np.array([x.wsp for x in ref_dlc(yaw=0)])
    mean_ = np.array([x.mean[key] for x in ref_dlc(yaw=0)])
    std_ = np.array([x.std[key] for x in ref_dlc(yaw=0)])
    max_ = np.array([x.max[key] for x in ref_dlc(yaw=0)])
    min_ = np.array([x.min[key] for x in ref_dlc(yaw=0)])

    plt.plot(wsp_, mean_, '.--k', label='no IPC')
    plt.plot(wsp_, mean_+std_, 'xk')
    plt.plot(wsp_, mean_-std_, 'xk')
    plt.plot(wsp_, max_, '.k')
    plt.plot(wsp_, min_, '.k')
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
              'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    for i, c in enumerate(dlc.unique(['controller'])):
        sims_ = dlc(controller=c, yaw=0, Kp=-0.05)
        wsp_ = np.array([x.wsp for x in sims_])
        mean_ = np.array([x.mean[key] for x in sims_])
        std_ = np.array([x.std[key] for x in sims_])
        max_ = np.array([x.max[key] for x in sims_])
        min_ = np.array([x.min[key] for x in sims_])

        plt.plot(wsp_, mean_, '.--', label=c[0], c=colors[i])
        plt.plot(wsp_, mean_+std_, 'x', color=colors[i])
        plt.plot(wsp_, mean_-std_, 'x', color=colors[i])
        plt.plot(wsp_, max_, '.', color=colors[i])
        plt.plot(wsp_, min_, '.', color=colors[i])


    plt.legend()
    #plt.savefig('Figures/Stats_{}.png'.format(key), dpi=200)
    plt.show()
    print()
    if save:
        raise NotImplementedError


if __name__ is '__main__':
    if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):

        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

    run(dlc, dlc_noipc)