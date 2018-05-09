# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:51:50 2018

@author: J

Analyses the mode shapes of the blade based on the
dtu_10mw_rwt_body_eigen file generated from HAWC2
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

SAVE = True

Z = [3.00000,6.00000,7.00004,8.70051,1.04020E+01,1.22046E+01,1.32065E+01,
1.50100E+01,1.82151E+01,2.14178E+01,2.46189E+01,2.78193E+01,3.10194E+01,
3.42197E+01,4.02204E+01,4.66217E+01,5.30232E+01,5.94245E+01,6.58255E+01,
7.22261E+01,7.90266E+01,8.05267E+01,8.20271E+01,8.35274E+01,8.50277E+01,
8.63655E+01]

L = max(Z)

N = 7 # Number of mode shapes to collect
# Read eigenmodes from HAWC2 eigenanalysis.
eigendata_filename = 'C:/JL0004/eig/dtu_10mw_rwt_body_eigen.dat'
with open(eigendata_filename) as f:
    data = f.read()
data = data.split('Eigenvectors for body : blade1')[1]
data = data.split('Mode nr:')[1:]

gamma = []
for i in range(N):
    gamma.append([])
    lines = data[i].split('\n')[2:-1]
    for line in lines:
        gamma[-1].append([float(x) for x in line.split()])
    gamma[-1] = np.array(gamma[-1])

# post processing of HAWC2 eigendata.
flapmode_d, edgemode_d = [], []
for i in range(N):
    #keep edgewise and flapwise components only
    gamma[i] = gamma[i][:,:2]
    # Normalise so that gamma(L) = 1, and sort between flap and edgewise modes.
    if max(abs(gamma[i][:, 1])) < max(abs(gamma[i][:, 0])):
        # if edgewise mode:
        gamma[i] /= gamma[i][-1, 0]
        edgemode_d.append(gamma[i])
    else: # if flapwise mode:
        gamma[i] /= gamma[i][-1, 1]
        flapmode_d.append(gamma[i])

# interpolate and find curvature (flapwise modes only):
flapmode, flap_curvature = [], []
z = np.linspace(min(Z), L, 100)
for mode in flapmode_d:
    flapmode.append(InterpolatedUnivariateSpline(Z, mode[:, 1], k=4))
    flap_curvature.append(flapmode[-1].derivative(2))


# plot curvature and mode
for i, mode in enumerate(flapmode_d):
    fig, ax = plt.subplots(2, 1, sharex=True)
    plt.subplots_adjust(hspace=0.05, left=0.2)
    #fig.suptitle('Flapwise Mode {}'.format(i+1))
    [x.axhline(y=0, lw=1, c='0.7', ls='--') for x in ax]
    ax[1].set_xlabel('z [m]')
    ax[0].set_ylabel('$\gamma(z)$ [-]')
    ax[1].set_ylabel('$ \partial^2\gamma/\partial z^2$ [-]')

    ax[0].plot(z, flapmode[i](z), lw=1)
    ax[1].plot(z, flap_curvature[i](z), lw=1)
    if SAVE:
        plt.savefig('../Figures/BladeModes/' + 'flapMode_{}.png'.format(i+1), dpi=200)
    plt.show(); print()

# print curvature at root
for i, mode in enumerate(flap_curvature):
    print('Flapwise Mode {}: Curvature at root: {:2.4e}'.format(i+1, float(mode(3))))


