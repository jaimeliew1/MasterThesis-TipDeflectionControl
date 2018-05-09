# -*- coding: utf-8 -*-
"""
Inverse shear wind profile calculation
Created on Wed May  9 09:21:53 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt

savePlots = True
saveShear = False
# Parameters
#U = 18 # free wind speed at hub height [m/s]
T = 12 # gust length [s]
alpha = 0.2 # power law exponent [-]
beta = 6.4
D = 178 # rotor diameter [m]
zhub = 119 # Hub height [m]
Iref = 0.16 # Turbulence intensity [-]
A = 42 # longitudinal turbulence scale parameter [m]

def InverseShearProfile(z, t, U=18):

    sigma = Iref * (0.75*U + 5.6) # Turbulence standard deviation (NTM)
    if t < T:
        V = U*(z/zhub)**alpha - (z-zhub)/D*(2.5 + 0.2*beta*sigma*(D/A)**0.25)*(1-np.cos(2*np.pi*t/T))
    else:
        V = U*(z/zhub)**alpha

    V[z==0] = 0
    return V

z = np.arange(0, zhub + D/2 + 30, 10)
t = np.linspace(0, 1.5*T, 100)


wsp = np.arange(4, 27, 2)
for U in wsp:
    V = InverseShearProfile(z, 6, U)
    Vref = InverseShearProfile(z, 0, U)
    plt.figure(figsize=(4, 4))
    plt.subplots_adjust(left=0.15)
    plt.xlim(0, 30)
    plt.xlabel('Wind speed [m/s]')
    plt.ylabel('Height [m]')
    plt.plot(V, z, label='Inverse shear')
    plt.plot(Vref, z, '--r', label='Power law')
    plt.axhline(y=zhub, lw=1, ls='--', c='k')
    plt.axhline(y=zhub + D/2, lw=1, ls='-', c='k')
    plt.axhline(y=zhub - D/2, lw=1, ls='-', c='k')
    plt.legend()
    if savePlots:
        plt.savefig('../Figures/InverseShearProfile_{}.png'.format(U), dpi=200)
    plt.show(); print()

#%% write shear file
if saveShear:
    template_filename = 'InverseShearProfile_Template.txt'
    Dir = 'C:/JL0004/data/'

    with open(Dir + template_filename) as f:
        template = f.read()

    for U in wsp:
        V = InverseShearProfile(z, T/2)/U
        string = ''
        for v in V:
            string += '{:2.6E} {:2.6E} {:2.6E}\n'.format(v, v, v)
        text = template.replace('{Profile}', string)
        with open(Dir + 'InverseShearProfile_{}.txt'.format(U), 'w') as f:
            f.write(text)
