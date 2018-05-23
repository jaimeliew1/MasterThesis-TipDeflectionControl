# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:52:45 2018

@author: J
TODO

"""

import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from JaimesThesisModule.Misc import readHawc2Res
from Configuration.Config import Config

plt.rc('text', usetex=True)
save = True

channels = {
    't'         : 1,    #time [s]
    'wsp'       : 15,   #wind speed [m/s]
    'RBM1'      : 26,   #root bending moment - blade 1 [kNm]
    'RBM2'      : 29,
    'RBM3'      : 32,
    'TD1'       : 49,   #Tip deflection - blade 1 [m]
    'TD2'       : 52,
    'TD3'       : 55,
    'pitch1'    :  4,   #pitch angle blade 1 [deg]
    'pitch2'    :  6,
    'pitch3'    :  8,
    'IPCDem1'   : 99,   #IPC pitch demand - blade 1 [rad]
    'IPCDem2'   : 100,
    'IPCDem3'   : 101}


dir_res = Config.modelpath + 'res/Pitchstep/'
dir_mat = 'Data/'

# get files with the filename form 'pitchstep_xx' where xx is the wind speed
# of the simulation.
resFiles = [x[:-4] for x in os.listdir(dir_res) if x.endswith('.sel')]
resFiles = [x for x in resFiles if x.startswith('pitchstep_lin')]

#resFiles = ['pitchstep_04', 'pitchstep_06']
#resFiles = ['pitchstep_06']

wsps = [int(x.split('_')[2]) for x in resFiles]
print('Result files found:')
[print(wsp, x) for wsp, x in zip(wsps, resFiles)]

# Load results for each windspeed
resData = []
for file in resFiles:
    resData.append(readHawc2Res(dir_res + file, channels))

# extract just the input and output timeseries, and remove forst 110 seconds
t, x, y = [], [], []

for data in resData:
    t.append(np.array(data.t))
    x.append(np.array(data.IPCDem1)[t[-1] > 110])
    y.append(np.array(data.TD1)[t[-1] > 110])
    #y2.append(np.array(data.TD2)[t[-1] > 110])
    t[-1] = t[-1][t[-1] > 110]

tpeak, tpeak2 = [], [] #indices of the overshoot to test linearity
ypeak, ypeak2 = [], []
for i in range(len(x)):
    x[i] = x[0] - x[0][0]
    y[i] -= y[i][0]
    t[i] = t[i] - 110

    j = np.argmin(y[i])
    tpeak.append(t[i][j])
    tpeak2.append(t[i][j + 4000])
    ypeak.append(y[i][j])
    ypeak2.append(y[i][j + 4000])



for i, wsp in enumerate(wsps):
    fig, axes = plt.subplots(2,1, sharex=True)
    plt.subplots_adjust(hspace=0.1)
    axes[0].set_xlim([0, 90])
    axes[0].set_ylim([-0.01, 0.03])
    #axes[1].set_ylim([-1.5, 1 ])
    axes[0].plot(t[i], x[i])
    axes[1].plot(t[i], y[i])

    #axes[1].plot([tpeak[i], tpeak2[i]], [ypeak[i], ypeak2[i]], 'xk')
    #axes[1].text(tpeak[i], ypeak[i], '{:2.3f}'.format(ypeak[i]))
    #axes[1].text(tpeak2[i], ypeak2[i], '{:2.3f}'.format(ypeak2[i]))

    fig.suptitle('$U = {}$'.format(int(resFiles[i][-2:])))
    axes[1].set_xlabel('Time [s]')
    axes[0].set_ylabel('$\~{x}(t) [rad]$')
    #axes[1].set_ylabel('$\~{y}(t) [m]$') # UNITS CHANGED
    axes[1].set_ylabel('$\~{y}(t) [kNm]$')
    #if True:
        #plt.savefig('../Figures/systemIdentification/pitchstep_RBM_{}.png'.format(wsp), dpi=200)
    plt.show(); print()
# save results to a matlab .m file

if save:
    for i, file in enumerate(resFiles):
        sio.savemat(dir_mat + file + '.mat',
                    {'t':t[i], 'x':x[i], 'y':y[i], 'wsp': wsps[i]})

#%%
for i, wsp in enumerate(wsps):
    print('{:2.3f} & {:2.3f} & {:2.3f} \\\\'.format(ypeak[i], ypeak2[i], ypeak[i]/ypeak2[i]))