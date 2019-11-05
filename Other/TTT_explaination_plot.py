# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 12:27:12 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)

offset = 40 #deg
pitchAmp = 0.4

fig, ax = plt.subplots(3, 1, sharex=True, figsize=[6,7])
plt.subplots_adjust(hspace=0.05)

# loop for each blade plot
for i in [0, 1, 2]:
    # generate sinusoids
    azim = np.linspace(0, 360)
    pitch = pitchAmp*np.sin(np.deg2rad(azim + offset + i*120))
    td = np.sin(np.deg2rad(azim + i*120))

    # Get key locations for annotation
    a = (210 - offset, pitchAmp)
    b = (210 - offset, 0)
    c = (210, 0)
    d = (210, 1)


    # Plot sinusoids
    ln1 = ax[i].plot(azim, td, label=r'Desired tip deflection, $r(t)$')
    ax2 = ax[i].twinx()
    ln2 = ax2.plot(azim, pitch, '--', c='tab:orange', label='Required tip deflection reference, $\\tilde{r}(t)$')


    # Additional settings
    ax[i].set_ylim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax[i].set_xlim(0, 360)
    ax[i].axhline(0, lw=1, c='0.7')

    ax[i].set_yticks([])
    ax2.set_yticks([])

    ax[i].set_ylabel('Tip Deflection [m]')
    ax2.set_ylabel(f'Blade {i+1}')
    

    if i==0:
        lns = ln1+ln2
        labs = [l.get_label() for l in lns]
        ax[i].legend(lns, labs, loc=0)
fig.text(0.5, 0.06, 'Rotor azimuth angle, $\psi$ [deg]', ha='center', rotation='horizontal')

# annotations
ax[2].annotate(s='', xy=a, xytext=b, xycoords = 'data',
  textcoords = 'data',arrowprops=dict(arrowstyle='<->', shrinkB=0, shrinkA=0))

ax[2].annotate(s='', xy=b, xytext=c, xycoords = 'data',
  textcoords = 'data',arrowprops=dict(arrowstyle='<->', shrinkB=0, shrinkA=0))

ax[2].annotate(s='', xy=c, xytext=d, xycoords = 'data',
  textcoords = 'data',arrowprops=dict(arrowstyle='<->', shrinkB=0, shrinkA=0))

ax[2].text(a[0] - 5, pitchAmp/2 - 0.1, '$\\frac{A_r}{\\alpha}$', horizontalalignment='right',
  verticalalignment='center', fontsize=15)

ax[2].text(a[0] + offset/2, -0.1, '$\\beta$', horizontalalignment='center',
  verticalalignment='top', fontsize=14)

ax[2].text(d[0] + 2, 1/2 - 0.1, '$A_r$', horizontalalignment='left',
  verticalalignment='center', fontsize=14)


# Save
plt.savefig('../Figures/TTT_explaination_plot.png', dpi=200, bbox_inches='tight')



plt.rc('text', usetex=False)
