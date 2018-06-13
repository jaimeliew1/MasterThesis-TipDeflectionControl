# -*- coding: utf-8 -*-
"""
DLC13 (ETM)for DTU10MW turbine with first generation of controllers
"""

from JaimesThesisModule import PreProc

# DLC parameters.

basename = 'dlc13_1'

fn_ = basename + '_{:03d}_{}_{:02d}_{:03d}_{}'
fn_func = lambda x: fn_.format(x['yaw'], x['controller'], x['wsp'], int(abs(x['Kp'])*1000), x['seed'])

Constants = {'Tstart'   :   100,
             'Tstop'    :   700,
             'Nx'       :   8192,
             'logfolder':   './log/dlc13_1/',
             'resfolder':   './res/dlc13_1/',
                 }

Variables = {
             'controller'   : ['ipcpi', 'ipc04', 'ipc07'],
             'Kp'           : [-1],
             'yaw'          : [0],
             'wsp'          : [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
             '_seed'        : [1, 2, 3]}


Functionals = {'seed'       : lambda x: 1000*x['_seed'] + x['wsp'],
              'Tint'        : lambda x: 2*0.16*(0.072*(10/2+3)*(x['wsp']/2 - 4) +10)/x['wsp'],
              'dx'          : lambda x: x['wsp'] * x['Tstop'] / x['Nx'],
              'filename'    : fn_func}

#%% Preprocessing
manifest = PreProc.Manifest(basename, Constants, Variables, Functionals)
manifest.printOverview()

manifest.checkTemplate('../Manifests/Master.htc')
manifest.missingRes()
manifest.save_csv()
manifest.generate_htc_files('../Manifests/Master.htc', overwrite=True)
