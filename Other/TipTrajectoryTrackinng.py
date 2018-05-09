# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:45:37 2018

@author: J
Todo: a different function for estimating deformation using:
    -strain gauge sensor
    -tip deflection sensor
    -both


"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule.Misc import readHawc2Res
import time



channels = {'t'         : 1,    #time [s]
            'Azim'      :  2,   #rotor azimuth angle [deg]
            'TD1'       : 49,   #Tip deflection - blade 1 [m]
            'TD2'       : 52,
            'TD3'       : 55,
            'TowerTip'  :118}


data = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/template',  channels)

data2 = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/tracking_4',  channels)

data3 = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/tracking_4_trunc',  channels)

td = data[['TD1', 'TD2','TD3']].as_matrix()
td2 = data2[['TD1', 'TD2','TD3']].as_matrix()
td3 = data3[['TD1', 'TD2','TD3']].as_matrix()

td -= np.reshape(td.mean(1), [-1,1])
td2 -= np.reshape(td2.mean(1), [-1,1])
td3 -= np.reshape(td3.mean(1), [-1,1])

plt.figure()
plt.plot(data.Azim, td[:,0], '.', ms=1)
plt.plot(data2.Azim, td2[:,0], '.', ms=1)
plt.plot(data3.Azim, td3[:,0], '.', ms=1)
plt.show(); print()

plt.figure()
plt.plot(data.Azim, td3[:, 0] - td[:, 0], '.', ms=1)
plt.show(); print()
ref = min(data.TowerTip)
print(min(data.TowerTip) - ref)
print(min(data2.TowerTip) - ref)
print(min(data3.TowerTip) - ref)