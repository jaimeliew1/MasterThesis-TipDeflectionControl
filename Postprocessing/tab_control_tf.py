# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 18:43:14 2018

@author: J
"""
from Modelling import BladeModel, OLResponse
from importlib import import_module
from JaimesThesisModule import ControlDesign, PostProc
import numpy as np
from scipy import signal, interpolate

def Spectrum(sim, Fs = 100):
    Ys = []
    channels =  {'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    for seed in sim:
        data = seed.loadFromSel(channels)
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)
            f, Py = signal.welch(data[key], Fs, nperseg=1024*8)
            Ys.append(np.sqrt(Fs*Py/60000))

    Yave = np.mean(Ys, axis=0)
    Yol = interpolate.interp1d(f, Yave, kind='linear', bounds_error=False)

    return Yol



Modules = ['IPC_PI',
           'IPC04',
           'IPC09',
           'IPC10',
           'IPC11',
           'IPC07',]

ControllerName = [ 'ipcpi',
                   'ipc04',
                   'ipc09',
                   'ipc10',
                   'ipc11',
                   'ipc07',]

latexName = ['$C_{PI}$',
             '$C_{f1p}$',
             '$C_{f2p}$',
             '$C_{f3p}$',
             '$C_{f4p}$',
             '$C_{2}$',
             ]

def getData():
    f1p = 0.16
    fs = f1p*np.array([1, 2, 3, 4])
    X = []
    P = BladeModel.Blade(wsp=18)
    Yol = OLResponse.Response(18)

    # loop over each controller
    for i, mod_name in enumerate(Modules):
        X.append({})


        # load linear closed loop system
        module = import_module('Controllers.' + mod_name)
        C = module.make()
        sys = ControlDesign.Turbine(P, C)

        X[i]['sm'] = sys.sm
        X[i]['linear'] = list(sys.performance(f1p))


        # load HAWC2 closed loop system results
        dlc = PostProc.DLC('dlc11_1')
        Sim = dlc(wsp=18, controller=ControllerName[i])[0]
        Ycl = Spectrum(Sim)
        X[i]['HAWC2'] = [Ycl(f)/Yol(f)-1 for f in fs]

    return X


if __name__ == '__main__':
    #X = getData()
    prototype = '''\\multirow{2}{*} {!NAME} & Linear &    !LINEAR & !SM\\\\
                       & HAWC2  &   !HAWC2 & - \\\\ \hline'''

    for i, C in enumerate(X):
        text = prototype
        text = text.replace('!NAME', latexName[i])
        text = text.replace('!LINEAR', ' & '.join([f'{x*100:2.2f}' for x in C['linear']]))
        text = text.replace('!HAWC2',  ' & '.join([f'{x*100:2.2f}' for x in C['HAWC2']]))

        text = text.replace('!SM', '{:2.2f}'.format(C['sm']))
        print(text)
