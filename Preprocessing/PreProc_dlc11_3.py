# -*- coding: utf-8 -*-
"""
DLC11 for DTU10MW turbine with tip trajectory tracking control.
"""

from JaimesThesisModule import PreProc

# DLC parameters.

basename = 'dlc11_3'

fn_ = basename + '_{}_a{:01d}_{:02d}_{}'
fn_func = lambda x: fn_.format(x['controller'], x['_amp'], x['wsp'], x['seed'])

def amp(x):
    if x['controller'] == 'ipcpi':
        return 1.42
    if x['controller'] == 'ipc04':
        return 1.12
    if x['controller'] == 'ipc07':
        return 1.39


Constants = {'Tstart'   :   100,
             'Tstop'    :   700,
             'Nx'       :   8192,
             'logfolder':   './log/dlc11_3/',
             'resfolder':   './res/dlc11_3/',
             'Kp'       :   -1,
             'yaw'      :   0,
             'Phase'    :   0
                 }

Variables = {
             'controller'   : ['ipcpi', 'ipc04', 'ipc07'],
             'wsp'          : [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
             '_seed'        : [1, 2, 3],
             '_amp'         : [1, 2, 3, 4] }


Functionals = {'seed'       : lambda x: 1000*x['_seed'] + x['wsp'],
              'Tint'        : lambda x: (0.75*x['wsp'] + 5.6)*0.16/x['wsp'],
              'dx'          : lambda x: x['wsp'] * x['Tstop'] / x['Nx'],
              'Amplitude'   : lambda x: amp(x)*x['_amp'],
              'filename'    : fn_func}

#%% Preprocessing
manifest = PreProc.Manifest(basename, Constants, Variables, Functionals)
manifest.printOverview()

manifest.checkTemplate('../Manifests/Master_TTT.htc')
manifest.missingRes()
manifest.save_csv()
manifest.generate_htc_files('../Manifests/Master_TTT.htc', overwrite=True)
