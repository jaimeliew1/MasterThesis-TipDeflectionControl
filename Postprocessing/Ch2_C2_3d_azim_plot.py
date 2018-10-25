# -*- coding: utf-8 -*-
"""
Creates plots of each blade RBM and TD versus azimuth angle as a hexbin plot.
todo: implemment this properly.

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from JaimesThesisModule import PostProc


R = 196
def binCyclicalData(T, Y, width=1):

    X = np.arange(0, 360, width)
    dat = {k:[] for k in X}
    for t, y in zip(T, Y):
        Bin = 0
        if t%360 != 0:
            Bin =X[X<t%360][-1]
        dat[Bin].append(y)
    return dat


def cyclicalMinMax(X, Y):
    hist = binCyclicalData(X, Y)
    azim = list(hist.keys())
    Max = [np.max(v) for v in hist.values()]
    Min = [np.min(v) for v in hist.values()]
    Mean = [np.mean(v) for v in hist.values()]

    return azim, Min, Max, Mean



def azim2cart(azim, r=10):
    x = r*np.sin(np.deg2rad(azim))
    y = -r*np.cos(np.deg2rad(azim))

    return x, y

def run(dlc, dlc_noipc, SAVE=None):

   pass



if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')

    #td, rbm = run(dlc, dlc_noipc, SAVE=False)

    wsp=20
    channels = {'Azim': 2,
                'RBM1'      : 26,
                'RBM2'      : 29,
                'RBM3'      : 32,
                'TD1'       : 49,
                'TD2'       : 52,
                'TD3'       : 55}
    # get ref sim data
    ref = dlc_noipc(wsp=wsp)[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim = data.Azim
            rbm = data[['RBM1', 'RBM2', 'RBM3']].as_matrix()
            td = -data[['TD1', 'TD2', 'TD3']].as_matrix()
        azim = np.append(azim, data.Azim)
        rbm = np.append(rbm, data[['RBM1', 'RBM2', 'RBM3']].as_matrix(), 0)
        td = np.append(td, -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)


    # get controlled sim data
    ref = dlc(wsp=wsp, controller='ipc07')[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim1 = data.Azim
            rbm1 = data[['RBM1', 'RBM2', 'RBM3']].as_matrix()
            td1 = -data[['TD1', 'TD2', 'TD3']].as_matrix()
        azim1 = np.append(azim1, data.Azim)
        rbm1 = np.append(rbm1, data[['RBM1', 'RBM2', 'RBM3']].as_matrix(), 0)
        td1 = np.append(td1, -data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)

    td -= np.reshape(td.mean(1), [-1, 1])
    td1 -= np.reshape(td1.mean(1), [-1, 1])
    # Set up plot



    Azim_mm1, Min1, Max1, Mean1 = cyclicalMinMax(azim, td[:, 0])
    Azim_mm2, Min2, Max2, Mean2 = cyclicalMinMax(azim1, td1[:, 0])
    xs, ys = azim2cart(Azim_mm1, r=R)
    zs = np.array(Mean1)

    rp_x, rp_y = np.meshgrid([-2*R, 2*R], [-2*R, 2*R])
    # Code to plot the 3D polygons
    fig = plt.figure()
    ax = Axes3D(fig)



    ax.plot(xs, zs, ys)
    ax.plot(xs, Mean2, ys)
    ax.plot(xs, np.zeros(len(xs)), ys, '--k')
    ax.set_ylim(-5,5)
    ax.view_init(elev=15, azim=20)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.set_axis_off()

    plt.savefig('tipdeflection_3d.png', dpi=300)

