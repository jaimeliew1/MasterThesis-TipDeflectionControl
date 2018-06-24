# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 18:43:14 2018

@author: J
"""

from JaimesThesisModule import PostProc
import numpy as np

latexName = [
             '$C_{f1p}$',
             '$C_{2}$',
             ]




def get_tcl_data_from_sim(sim):
    tcl = []
    for seed in sim:
        data = seed.loadFromSel(channels={'tcl':111})
        tcl += lowerPeaks(data.tcl)
    return tcl



def lowerPeaks(X):
    peaks = []
    for i, x in enumerate(X):
        if i == 0 or i == len(X)-1:
            continue

        if (X[i-1] >= x) and (X[i+1] > x):
            peaks.append(x)
    return peaks




def getData(dlc_noipc, dlc1, dlc2, wsp=20):

    # no ipc case
    tcl_noipc = get_tcl_data_from_sim(dlc_noipc(wsp=wsp)[0])

    # ipc04 tower clearances
#    c = 'ipc04'
#    tcl1 = {0:get_tcl_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
#    for a in [1, 2, 3, 4]:
#        tcl1[a] = get_tcl_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])

    # ipc04 tower clearances
    c = 'ipc07'
    tcl = {0:get_tcl_data_from_sim(dlc1(controller=c, wsp=wsp)[0])}
    for a in [1, 2, 3, 4]:
        tcl[a] = get_tcl_data_from_sim(dlc2(controller=c, wsp=wsp, _amp=a)[0])

    # extract statistical data
#    mean = {'noipc': np.mean(tcl_noipc), 'Cf1p':{}, 'C2':{}}
#    Min = {'noipc': np.min(tcl_noipc), 'Cf1p':{}, 'C2':{}}
#
#    for amp in [0, 1, 2, 3, 4]:
#        mean['Cf1p'][amp] = np.mean(tcl1[amp])
#        mean['C2'][amp] = np.mean(tcl2[amp])
#
#        Min['Cf1p'][amp] = np.min(tcl1[amp])
#        Min['C2'][amp] = np.min(tcl2[amp])

    # no ipc
    mean = [np.mean(tcl_noipc)]
    Min = [np.min(tcl_noipc)]

    # TTT
    for amp in [0, 1, 2, 3, 4]:
        mean.append(np.mean(tcl[amp]))
        Min.append(np.min(tcl[amp]))

    return mean, Min




def printLatexTable(mean, Min, name):
    prototype = '''\\multirow{2}{*} {!NAME} & mean &    !MEAN \\\\
                       & min  &   !MIN \\\\ \hline'''

# first bit with no control
#    text = prototype
#    text = text.replace('!NAME', 'no IPC')
#    text = text.replace('!MEAN', ' {:2.2f} & - & - & - & -'.format(mean['noipc']))
#    text = text.replace('!MIN', ' {:2.2f} & - & - & - & -'.format(Min['noipc']))
#    print(text)



    text = prototype
    text = text.replace('!NAME', name)
    text = text.replace('!MEAN', ' & '.join([f'{x:2.2f}' for x in mean]))
    text = text.replace('!MIN',  ' & '.join([f'{x:2.2f}' for x in Min]))

    print(text)


if __name__ == '__main__':
    dlcs = {
    'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}



    mean, Min = getData(dlcs['dlc11_0'], dlcs['dlc11_1'], dlcs['dlc11_3'])
    printLatexTable(mean, Min, name='Normal Shear')

    mean, Min = getData(dlcs['dlc15_0'], dlcs['dlc15_1'], dlcs['dlc15_2'])
    printLatexTable(mean, Min, name='Inverse Shear')

