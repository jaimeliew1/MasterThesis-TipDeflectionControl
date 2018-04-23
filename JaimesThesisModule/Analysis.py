import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import griddata

opData = np.array([  [4.0, 0.10],
                     [6.0, 0.10],
                     [8.0, 0.1213],
                     [10.0, 0.1517],
                     [12.0, 0.16],
                     [14.0, 0.16],
                     [16.0, 0.16],
                     [18.0, 0.16],
                     [20.0, 0.16],
                     [22.0, 0.16],
                     [24.0, 0.16],
                     [26.0, 0.16]])

def plotRotorFreq(nP=1, ax=None):
    F1p = opData[-1,1]
    if ax is None:
        ax = plt.gca()
    for n in range(nP):
        ax.plot(opData[:,0], (n+1) * opData[:,1], '--', color='0.2', lw=0.5)
        ax.text(11, 0.01 + F1p*(n+1), '{}P'.format(n+1), color='0.2')

def plotShutdown(sims, ax=None):
    if ax is None:
        ax = plt.gca()
    for sim in sims:
        ax.plot([sim.wsp]*2, [0, 0.7], 'k', lw=35.5, alpha=sim.shutdown)

def makeDataGrid(sims, axis='WspFreqReq', key='RBM1'): #!!! UNTESTED
    if axis.lower() =='wspfreqreq'.lower():
            X_ = [x.wsp for x in sims]
            Y_ = sims[0].fData.f.values
            X, Y = np.meshgrid(X_, Y_)
            Z = np.zeros(X.shape)
            for i, sim in enumerate(sims):
                Z[:,i] = sim.fData[key]


    return X, Y, Z
def SpectralContour3(X, Y, Z, ax=None):
    clip = 1
    zmax = 100#clip*max(abs(Z.max()), abs(Z.min()))

    norm = colors.Normalize(vmin=-zmax, vmax=zmax,clip=True)
    levels = np.linspace(-zmax, zmax, 21)
    CP = ax.contourf(X, Y, Z, levels,
                     norm=norm, cmap='viridis')
    ax.contour(X, Y, Z, levels, colors='k', linewidths=0.1)

    CB = plt.colorbar(CP)
    #CB.set_ticks(np.linspace(0, Z.max(), 6))
    CB.set_label('Change in PSD [%]')
def SpectralContour2(X, Y, Z, ax=None):

    zmax = Z.max()
    clip = 0.2
    norm = colors.Normalize(vmin=0, vmax=clip*zmax,clip=False)
    levels = np.concatenate((np.linspace(0, clip*zmax,21),
                             np.linspace(1.1*clip*zmax, zmax, 11)))
    CP = ax.contourf(X, Y, Z, levels,
                     norm = norm, cmap='summer')
    ax.contour(X, Y, Z, levels, colors='k', linewidths=0.1)

    CB = plt.colorbar(CP)
    #CB.set_ticks(np.linspace(0, Z.max(), 6))
    CB.set_label('Power Spectral Density [kNm^2/Hz]')


def SpectralContour(sims, key, ax=None):
    Y_ = sims[0].fData.f.values
    X_ = [x.wsp for x in sims]
    Z = np.zeros((len(Y_), len(X_)))
    X, Y = np.meshgrid(X_, Y_)
    for i, sim in enumerate(sims):
        Z[:,i] = sim.fData[key]

    zmax = Z.max()
    clip = 0.2
    norm = colors.Normalize(vmin=0, vmax=clip*zmax,clip=False)
    levels = np.concatenate((np.linspace(0, clip*zmax,21),
                             np.linspace(1.1*clip*zmax, zmax, 11)))
    CP = ax.contourf(X, Y, Z, levels,
                     norm = norm, cmap='summer')
    ax.contour(X, Y, Z, levels, colors='k', linewidths=0.1)

    CB = plt.colorbar(CP)
    #CB.set_ticks(np.linspace(0, Z.max(), 6))
    CB.set_label('Power Spectral Density [kNm^2/Hz]')



        #            ax1.text(11, 0.01 + F1p*(i+1), '{}P'.format(i+1), color='0.2')
#            ax1.plot(opData[:,0], (i+1)*opData[:,1], '--', color='0.2', lw=0.5)
#def SpectralSurface(Sims, Data_f, key='RBM1', interp_f=None, interp_wsp=None):
#    # Generates a spectral surface with frequency on the y axis, wind speed
#    # on the x axis, and spectral density on the z axis.
#    Y_ = Data_f[0].f
#    X_ = Sims.wsp
#    Z = np.zeros((len(Y_), len(X_)))
#    X, Y = np.meshgrid(X_, Y_)
#    for i, (ind, sim) in enumerate(Sims.iterrows()):
#        Z[:,i] = (Data_f[ind][key])
#
#    if any([interp_f, interp_wsp]):
#        if interp_wsp is not None:
#            Xint = np.arange(X.min(), X.max()+0.01, interp_wsp)
#        else:
#            Xint = X_
#        if interp_f is not None:
#            Yint = np.linspace(0, Y.max(), interp_f)
#        else:
#            Yint = Y_
#        Xint, Yint = np.meshgrid(Xint, Yint)
#        Zint        = griddata(np.array([X.ravel(), Y.ravel()]).T, Z.ravel(),
#                               (Xint, Yint), method='cubic')
#        Zint[Zint<0] = Z.min()
#        return Xint, Yint, Zint
#    return X, Y, Z
#
#def SpectralSurface_plot(X, Y, Z, title=''):
#    plt.figure()
#    plt.title(title); plt.grid(); plt.autoscale(tight=True)
#    plt.xlabel('Frequency [Hz]'); plt.ylabel('Power Spectral Density [kNm^2/Hz]')
#    for i in range(Z.shape[1]):
#        plt.plot(Y[:,i], Z[:,i], label='{}m/s'.format(X[0,i]))
#    #plt.legend()
#
#def SpectralContour(X, Y, Z, opData=None, title='',save=None, clip=0.5, zmax=None):
#    fig = plt.figure(figsize=[7,5])
#    ax = fig.gca()
#    ax.set_title(title)
#    ax.set_xlim([6,26])
#    if zmax is None:
#        zmax = Z.max()
#
#    ax.set_ylabel('Frequency [Hz]'); ax.set_xlabel('Wind speed [m/s]')
#    fig.tight_layout()
#
#    if opData is not None:
#        F1p = opData[-1,1]
#        for i in range(4):
#            plt.text(11, 0.01 + F1p*(i+1), '{}P'.format(i+1), color='0.2')
#            plt.plot(opData[:,0], (i+1)*opData[:,1], '--', color='0.2', lw=0.5)
#
#    norm = colors.Normalize(vmin=0, vmax=clip*zmax,clip=False)
#    levels = np.concatenate((np.linspace(0, clip*zmax,21),
#                             np.linspace(1.1*clip*zmax, zmax, 11)))
#    CP = ax.contourf(X, Y, Z, levels,
#                     norm = norm, cmap='summer', antialiased=False)
#    ax.contour(X, Y, Z, levels,colors='k',linewidths=0.1)
#
#    CB = fig.colorbar(CP)
#    #CB.set_ticks(np.linspace(0, Z.max(), 6))
#    CB.set_label('Power Spectral Density [kNm^2/Hz]')
#    if save is not None:
#        fig.savefig(save, dpi=200)
#
#def SpectralContourAnim(X, Y, Z, opData=None, title='', save=None, fps=10, clip=1):
#    figsize=np.array([9,5])*0.8
#    fig, (ax1,ax2) = plt.subplots(1,2, figsize=figsize, sharey=True,
#          gridspec_kw = {'width_ratios':[2, 1]})
#    fig.subplots_adjust(wspace=0.02)
#    fig.suptitle(title)
#    #fig.tight_layout()
#    ax1.set_xlim([6,26])
#    ax1.set_ylim([0, Y.max()])
#    ax2.set_ylim([0, Y.max()])
#    ax1.set_ylabel('Frequency [Hz]'); ax1.set_xlabel('Wind speed [m/s]')
#    ax2.yaxis.set_visible('off')
#    ax2.yaxis.set_tick_params(left='off')
#    ax2.set_xlim([0,Z.max()])
#    ax2.set_xlabel('Power Spectral Density [m^2/Hz]')
#    if opData is not None:
#        F1p = opData[-1,1]
#        for i in range(4):
#            ax1.text(11, 0.01 + F1p*(i+1), '{}P'.format(i+1), color='0.2')
#            ax1.plot(opData[:,0], (i+1)*opData[:,1], '--', color='0.2', lw=0.5)
#
#    norm = colors.Normalize(vmin=0, vmax=clip*Z.max(),clip=False)
#    levels = np.concatenate((np.linspace(0, clip*Z.max(),21),
#                             np.linspace(1.1*clip*Z.max(), Z.max(), 11)))
#    CP = ax1.contourf(X, Y, Z, levels,
#                     norm = norm, cmap='summer', antialiased=False)
#    ax1.contour(X, Y, Z, levels,colors='k',linewidths=0.1)
#
#    wsp = X[0, :]
#    F1P = np.interp(wsp, opData[:, 0], opData[:, 1])
#    lines = []
#    lines.append(ax1.plot([], [], lw=1, ls='--', color='tab:orange'))
#    lines.append(ax2.plot([], [], lw=1,ls='--', color='tab:orange'))
#    lines.append(ax2.plot([], [], '--', color='0.2', lw=0.5))
#    lines.append(ax2.plot([], [], '--', color='0.2', lw=0.5))
#    lines.append(ax2.plot([], [], '--', color='0.2', lw=0.5))
#    lines.append(ax2.plot([], [], '--', color='0.2', lw=0.5))
#    lines.append(ax2.text(0, 0, '1P', color='0.2'))
#    lines.append(ax2.text(0, 0, '2P', color='0.2'))
#    lines.append(ax2.text(0, 0, '3P', color='0.2'))
#    lines.append(ax2.text(0, 0, '4P', color='0.2'))
#    lines.append(ax2)
#
#    def run(ind):
#        # update the data
#
#        lines[0][0].set_data([wsp[ind]]*2, [0, Y.max()])
#        lines[1][0].set_data(Z[:,ind], Y[:,ind])
#
#        lines[2][0].set_data([0, Z.max()], [1*F1P[ind]]*2)
#        lines[3][0].set_data([0, Z.max()], [2*F1P[ind]]*2)
#        lines[4][0].set_data([0, Z.max()], [3*F1P[ind]]*2)
#        lines[5][0].set_data([0, Z.max()], [4*F1P[ind]]*2)
#        lines[6].set_position([0.8*Z.max(), 1*F1P[ind]])
#        lines[7].set_position([0.8*Z.max(), 2*F1P[ind]])
#        lines[8].set_position([0.8*Z.max(), 3*F1P[ind]])
#        lines[9].set_position([0.8*Z.max(), 4*F1P[ind]])
#
#        print('\rAnimating: {:2.2f}'.format(wsp[ind]), end='')
#        return lines,
#    Writer = animation.writers['ffmpeg']
#    writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
#    ani = animation.FuncAnimation(fig, run, len(wsp), interval=100)
#    if save is not None:
#        try:
#            os.remove(save + '.gif')
#        except FileNotFoundError:
#            pass
#        ani.save(save + '.mp4', writer=writer,dpi=300)
#        os.system('ffmpeg -i {}.mp4 {}.gif'.format(save, save))
#        os.remove(save + '.mp4')