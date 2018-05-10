# -*- coding: utf-8 -*-
"""
Analyses and produces plots for a single controller in the dlc.
Created on Tue Apr 24 17:05:09 2018

@author: J
"""
from JaimesThesisModule import PostProc
import VerifyInverseShear, FatigueLoad_BarGraph, SpectralSurface, VsAzimuth
import PitchAngle, PowerOutput, EquivalentLoad_lifetime


def CompleteDataset(dlc, c):
    wsp_range = range(4, 27, 2)
    sims = dlc(controller=c, yaw=0)

    if not all(x.wsp in wsp_range for x in sims):
        return False
    else:
        return True

_locals = locals().keys()
if not all(x in _locals for x in ['dlc15_0', 'dlc15_1', 'dlc11_0']):
    dlc15_0 = PostProc.DLC('dlc15_0')
    dlc15_0.analysis(mode='fullload')

    dlc15_1 = PostProc.DLC('dlc15_1')
    dlc15_1.analysis(mode='fullload')

    dlc11_0 = PostProc.DLC('dlc11_0')
    dlc11_0.analysis(mode='fullload')


SAVE = False
c = 'ipc07'
import Controllers.IPC07 as IPC


if any(x.shutdown for x in dlc15_1(controller=c, yaw=0)):
    print('Some turbines shutdown')
else:
    print('No turbines shutdown')


if not CompleteDataset(dlc15_1, c):
    print('DATASET INCOMPLETE!')
else:
    pass
    VerifyInverseShear.run(dlc11_0, dlc15_0, SAVE=SAVE)
    FatigueLoad_BarGraph.run(dlc15_1, dlc15_0, c, SAVE=SAVE)
    SpectralSurface.run(dlc15_1, dlc15_0, c, SAVE=SAVE)
    VsAzimuth.run(dlc15_1, dlc15_0, c, SAVE=SAVE)
    #PitchAngle.run(dlc, dlc_noipc, c, SAVE=SAVE)
    EquivalentLoad_lifetime.run(dlc15_1, dlc15_0, c, SAVE=SAVE)
    #PowerOutput.run(dlc15_1, dlc15_0, c, SAVE=SAVE)