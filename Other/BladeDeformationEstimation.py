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

SAVE = True



Z = np.array([3.00000,6.00000,7.00004,8.70051,1.04020E+01,1.22046E+01,1.32065E+01,
1.50100E+01,1.82151E+01,2.14178E+01,2.46189E+01,2.78193E+01,3.10194E+01,
3.42197E+01,4.02204E+01,4.66217E+01,5.30232E+01,5.94245E+01,6.58255E+01,
7.22261E+01,7.90266E+01,8.05267E+01,8.20271E+01,8.35274E+01,8.50277E+01,
8.63655E+01])
L = Z[-1]

prebend = np.array([-1.22119E-02,
-2.49251E-02,
-2.73351E-02,
-2.82163E-02,
-2.13210E-02,
-1.28378E-02,
-7.70659E-03,
-4.88317E-03,
-1.80296E-02,
-5.01772E-02,
-9.41228E-02,
-1.48880E-01,
-2.14514E-01,
-2.90618E-01,
-4.62574E-01,
-6.88437E-01,
-9.60017E-01,
-1.28424E+00,
-1.66402E+00,
-2.10743E+00,
-2.65630E+00,
-2.78882E+00,
-2.92517E+00,
-3.06577E+00,
-3.20952E+00,
-3.33685E+00
])
mode1 = np.array([  3.01577241e-04,   1.05833597e-03,   1.41189356e-03,
         2.14330987e-03,   3.05374947e-03,   4.24113781e-03,
         5.01821367e-03,   6.67518727e-03,   1.06378266e-02,
         1.62043483e-02,   2.37919950e-02,   3.37396873e-02,
         4.65529851e-02,   6.25559382e-02,   1.02797870e-01,
         1.62590241e-01,   2.42746746e-01,   3.45554716e-01,
         4.71695682e-01,   6.19912449e-01,   7.97493967e-01,
         8.38288403e-01,   8.79559947e-01,   9.21169297e-01,
         9.62940584e-01,   1.00000000e+00])

mode2 = np.array([ -9.75079239e-04,  -3.16820451e-03,  -4.16423791e-03,
        -6.19344674e-03,  -8.66392308e-03,  -1.18122547e-02,
        -1.38342371e-02,  -1.80453409e-02,  -2.76498235e-02,
        -4.02276344e-02,  -5.60443473e-02,  -7.50795047e-02,
        -9.69879886e-02,  -1.21092581e-01,  -1.68781035e-01,
        -2.11869509e-01,  -2.26675576e-01,  -1.86053673e-01,
        -6.16834001e-02,   1.68084157e-01,   5.30830807e-01,
         6.21953650e-01,   7.16323098e-01,   8.13168683e-01,
         9.11690706e-01,   1.00000000e+00])

# d^2u/dz^2 at blade root
curve1, curve2 = 4.2827e-05, -1.0194e-04

EI = 6.1012e10

Delta = EI*(curve1 - curve2)

channels2 = {'t'         : 1,    #time [s]
            'Azim'      :  2,   #rotor azimuth angle [deg]
            'RBM1'      : 26,   #root bending moment - blade 1 [kNm]
            'RBM2'      : 29,
            'RBM3'      : 32,
            'TD1'       : 73,   #Tip deflection - blade 1 [m]
            'TD2'       : 99,
            'TD3'       : 125}

channels = {
            'B1_00'   : 48,
'B1_01'   : 49,
'B1_02'   : 50,
'B1_03'   : 51,
'B1_04'   : 52,
'B1_05'   : 53,
'B1_06'   : 54,
'B1_07'   : 55,
'B1_08'   : 56,
'B1_09'   : 57,
'B1_10'   : 58,
'B1_11'   : 59,
'B1_12'   : 60,
'B1_13'   : 61,
'B1_14'   : 62,
'B1_15'   : 63,
'B1_16'   : 64,
'B1_17'   : 65,
'B1_18'   : 66,
'B1_19'   : 67,
'B1_20'   : 68,
'B1_21'   : 69,
'B1_22'   : 70,
'B1_23'   : 71,
'B1_24'   : 72,
'B1_25'   : 73         }


def estimateDeformation(M, y, offset=-4483521.4983917726):
    # estimate blade deformation based on RBM [N] and
    # tip deflection [m] measurement
    # Rbm offset determined by minimizing the square error
    M = M + offset
    a1 = (M - EI*curve2*y)/Delta
    a2 = (-M + EI*curve1*y)/Delta
    #print(a1, a2, a2/a1)
    u =  a1*mode1 + a2*mode2

    return u

def estimateDeformation2(M, y):
    # estimate blade deformation based tip deflection [m] measurement only


    u = mode1*y

    return u

def estimateDeformation3(M, y, offset=-3029936.0653069587):
    # estimate blade deformation based RBM [Nm] measurement only
    # RBM offset determined to minimize the square error
    M = M + offset
    u = mode1*M/(EI*curve1)
    return u

data2 = readHawc2Res('C:/JL0004/res/fullspandeflectionsensors',  channels).as_matrix()
data = readHawc2Res('C:/JL0004/res/fullspandeflectionsensors',  channels2)


def plotDeformation(i, title='', save=None):
    RBM = -data.RBM1[i]*1000
    TD = data.TD1[i] - prebend[-1]
    est1 = estimateDeformation(RBM, TD) + prebend
    est2 = estimateDeformation2(RBM, TD) + prebend
    est3 = estimateDeformation3(RBM, TD) + prebend

    plt.figure(figsize=(4,4))
    plt.grid()
    plt.ylim(-3, 7)
    plt.xlim(0, 87)
    plt.title(title)
    plt.xlabel('Span [m]')
    plt.ylabel('Deformation [m]')
    plt.plot(Z, est2 )
    plt.plot(Z, est3)
    plt.plot(Z,est1)
    plt.plot(Z, data2[i, :], '--k')
    plt.legend(['TD sensor','RBM sensor', 'TD & RBM sensors', 'actual'], loc='upper left')

    if save:
        plt.savefig(save, dpi=200)
    plt.show(); print()




E1, E2, E3 = [], [], [] # integral error
plot = False
for i in range(0, len(data)):


    RBM = -data.RBM1[i]*1000
    TD = data.TD1[i] - prebend[-1]
    est1 = estimateDeformation(RBM, TD) + prebend
    est2 = estimateDeformation2(RBM, TD) + prebend
    est3 = estimateDeformation3(RBM, TD) + prebend

    E1.append(np.trapz(abs(est1-data2[i,:]), Z))
    E2.append(np.trapz(abs(est2-data2[i,:]), Z))
    E3.append(np.trapz(abs(est3-data2[i,:]), Z))


#%% error histogram
N = len(E1)
plt.figure()
plt.xlim([0, 30])
plt.hist(E1, 20, range=[0, 30], alpha=0.8, weights=1/N*np.ones(N),label='Strain Gauge + TD Sensor')
plt.hist(E2, 20, range=[0, 30], alpha=0.8, weights=1/N*np.ones(N),
         label='TD Sensor')
plt.hist(E3, 20, range=[0, 30], alpha=0.8, weights=1/N*np.ones(N), label='Strain Gauge')

plt.legend()
plt.xlabel('estimation error [$m^2$]')
plt.ylabel('Probability [-]')

if SAVE:
    plt.savefig('..\Figures\BladeDeformationEstimation\TD_RBM_Error.png', dpi = 200, bbox_inches='tight')
plt.show(); print()

#%% plot deformation with area difference
def plotDeformation2(Z, est, real, caption='', SAVE=False):
    fig, ax = plt.subplots(figsize=(4,4))
    plt.grid()
    plt.ylim(-3, 7)
    plt.xlim(0, 1)

    plt.xlabel('Nondimensional Span [-]')
    plt.xticks([0, 1/4, 2/4, 3/4, 1])
    ax.set_xticklabels([0, '$L/4$','$L/2$','$3L/4$', '$L$'])
    plt.ylabel('Deformation [m]')
    plt.plot(Z/L, est, label=caption)
    plt.plot(Z/L, real, '--k', label='Actual')
    plt.fill_between(Z/L, est1, data2[i, :], color='r', alpha=0.5, label='Error')
    ax.set_axisbelow(True)
    plt.legend()

    if SAVE:
        plt.savefig(f'..\Figures\BladeDeformationEstimation\{SAVE}.png', dpi = 200, bbox_inches='tight')
    plt.show(); print()



i = np.argmax(E1)
RBM = -data.RBM1[i]*1000
TD = data.TD1[i] - prebend[-1]
est1 = estimateDeformation(RBM, TD) + prebend
plotDeformation2(Z, est1, data2[i, :], 'Hybrid Sensor', 'Hybrid')

i = np.argmax(E2)
RBM = -data.RBM1[i]*1000
TD = data.TD1[i] - prebend[-1]
est1 = estimateDeformation2(RBM, TD) + prebend
plotDeformation2(Z, est1, data2[i, :], 'TD Sensor', 'TD')

i = np.argmax(E3)
RBM = -data.RBM1[i]*1000
TD = data.TD1[i] - prebend[-1]
est1 = estimateDeformation3(RBM, TD) + prebend
plotDeformation2(Z, est1, data2[i, :], 'Strain Gauge', 'StrainGauge')
#plt.legend(['TD sensor','RBM sensor', 'TD & RBM sensors', 'actual'], loc='upper left')




#%%
print('TD and RBM sensors:', np.mean(E1))
print('TD sensors:', np.mean(E2))
print('RBM sensors:', np.mean(E3))

#%% plot worst cases for each sensor
#plotDeformation(np.argmax(E1), save='..\Figures\BladeDeformationEstimation\TD_RBM_BladeDeformationEstimation.png')
#plotDeformation(np.argmax(E2), save='..\Figures\BladeDeformationEstimation\TD_BladeDeformationEstimation.png')
#plotDeformation(np.argmax(E3), save='..\Figures\BladeDeformationEstimation\RBM_BladeDeformationEstimation.png')