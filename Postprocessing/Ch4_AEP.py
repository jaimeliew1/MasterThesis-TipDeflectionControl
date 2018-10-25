# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:52:45 2018

@author: J
TODO

"""

import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
from Other.Weibull import wsp_probs


def get_pelec_data_from_sim(sim):
    x = []
    for seed in sim:
        data = seed.loadFromSel(channels={'Pelec':103})
        x += list(data['Pelec'].values/1e6)
    return x

def AEP(dlc, **kwargs):
    WSP = np.arange(4, 27, 2)

    Pmean = []
    for wsp in WSP:
        sim = dlc(wsp=wsp, **kwargs)[0]
        Pmean.append(np.mean(get_pelec_data_from_sim(sim)))

    prob = np.array(list(wsp_probs().values()))

    AEP =  8760*sum(Pmean*prob) # in MW hours

    return AEP


def run(dlcs, SAVE=False):
    #dlc_noipc = dlcs['dlc11_0']
    aep_noipc = AEP(dlcs['dlc11_0'])
    aep = [AEP(dlcs['dlc11_1'], controller='ipc07')]
    for amp in [1,2,3,4]:
        aep.append(AEP(dlcs['dlc11_3'], controller='ipc07', _amp=amp))

    string = ''
    for aep_ in aep:
        string += f'{(aep_/aep_noipc - 1)*100:.2f}% &'

    print(string)


if __name__ is '__main__':
    dlcs = {'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3')}

    run(dlcs)


