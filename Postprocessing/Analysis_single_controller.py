# -*- coding: utf-8 -*-
"""
Analyses and produces plots for a single controller in the dlc.
Created on Tue Apr 24 17:05:09 2018

@author: J
"""
from JaimesThesisModule import PostProc
import CLResponse, FatigueLoad_BarGraph, SpectralSurface, VsAzimuth
import PitchAngle, PowerOutput, EquivalentLoad_lifetime


def CompleteDataset(dlc, c):
    wsp_range = range(4, 27, 2)
    sims = dlc(controller=c, yaw=0)

    if not all(x.wsp in wsp_range for x in sims):
        return False
    else:
        return True


if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis(mode='fullload')

    dlc = PostProc.DLC('dlc11_1')
    dlc.analysis(mode='fullload')



c = 'ipc04'
import Controllers.IPC04 as IPC



if not CompleteDataset(dlc, c):
    print('DATASET INCOMPLETE!')
else:
    CLResponse.run(dlc, dlc_noipc, c, IPC.make(), SAVE=True)
    FatigueLoad_BarGraph.run(dlc, dlc_noipc, c, SAVE=True)
    SpectralSurface.run(dlc, dlc_noipc, c, SAVE=True)
    VsAzimuth.run(dlc, dlc_noipc, c, SAVE=True)
    PitchAngle.run(dlc, dlc_noipc, c, SAVE=True)
    # TODO plot lifetime brgraph
    EquivalentLoad_lifetime.run(dlc, dlc_noipc, c, SAVE=True)
    #PowerOutput.run(dlc, dlc_noipc, c, SAVE=True)