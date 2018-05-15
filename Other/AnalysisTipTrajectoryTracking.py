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


data = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/tracking_nocontrol',  channels)

data2 = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/tracking_0',  channels)

data3 = readHawc2Res('C:/Dropbox/Uni/Masters/4 Thesis/HAWC2-Python-Simulation/DTU10MW_Turbine/res/template/tracking_3',  channels)

# load tip deflection time series from each sim and subtract mean
td = data[['TD1', 'TD2','TD3']].as_matrix()
td2 = data2[['TD1', 'TD2','TD3']].as_matrix()
td3 = data3[['TD1', 'TD2','TD3']].as_matrix()

td -= np.reshape(td.mean(1), [-1,1])
td2 -= np.reshape(td2.mean(1), [-1,1])
td3 -= np.reshape(td3.mean(1), [-1,1])

# Plot tip deflection vs azimuth angle
plt.figure()
plt.plot(data.Azim, td[:,0], '.', ms=1)
plt.plot(data2.Azim, td2[:,0], '.', ms=1)
plt.plot(data3.Azim, td3[:,0], '.', ms=1)
plt.show(); print()

plt.figure()
plt.plot(data.Azim, td2[:, 0] - td[:, 0], '.', ms=1)
plt.show(); print()
ref = min(data.TowerTip)
ref = 0
print(min(data.TowerTip) - ref)
print(min(data2.TowerTip) - ref)
print(min(data3.TowerTip) - ref)


def lowerPeaks(X):
    peaks = []
    for i, x in enumerate(X):
        if i == 0 or i == len(X)-1:
            continue

        if (X[i-1] > x) and (X[i+1] > x):
            peaks.append(x)
    return peaks

fig, ax = plt.subplots(3,1, sharex=True, figsize=[6, 6])
plt.subplots_adjust(hspace=0.1)
ax[0].hist(lowerPeaks(data.TowerTip), alpha=0.8, label='no control')
ax[1].hist(lowerPeaks(data2.TowerTip), alpha=0.8, label='disturbance rejection')
ax[2].hist(lowerPeaks(data3.TowerTip), alpha=0.8, label='disturbance rejection + tip tracking')
[a.legend() for a in ax]
ax[2].set_xlabel('Minimum Tower Clearance')
ax[2].set_xlim(2, 11)