# -*- coding: utf-8 -*-
"""
DLC11 for DTU10MW turbine root bending moment (RBM) based control. The
purpose of this DLC is to compare to tip deflection (TD) based control.
"""

from JaimesThesisModule import PreProc

# DLC parameters.

basename = 'dlc11_2'

fn_ = basename + '_{:03d}_{}_{:02d}_{:03d}_{}'
fn_func = lambda x: fn_.format(x['yaw'], x['controller'], x['wsp'], int(abs(x['Kp'])*1000), x['seed'])

Constants = {'Tstart'   :   100,
             'Tstop'    :   700,
             'Nx'       :   8192,
             'logfolder':   './log/dlc11_2/',
             'resfolder':   './res/dlc11_2/',
                 }

Variables = {
             'controller'   : ['ipc_rbm04', 'ipc_rbm05', 'ipc_rbm06',
                               'ipc_rbm07', 'ipc_rbm08','ipc_rbm09',
                               'ipc_rbm10', 'ipc_rbm11'],
             'Kp'           : [1], # Note: sign changed compared to TD control
             'yaw'          : [0],
             'wsp'          : [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
             '_seed'        : [1, 2, 3]}


Functionals = {'seed'       : lambda x: 1000*x['_seed'] + x['wsp'],
              'Tint'        : lambda x: (0.75*x['wsp'] + 5.6)*0.16/x['wsp'],
              'dx'          : lambda x: x['wsp'] * x['Tstop'] / x['Nx'],
              'filename'    : fn_func}

#%% Preprocessing
manifest = PreProc.Manifest(basename, Constants, Variables, Functionals)
manifest.printOverview()

manifest.checkTemplate('../Manifests/Master_RBM.htc')
manifest.missingRes()
manifest.save_csv()
manifest.generate_htc_files('../Manifests/Master_RBM.htc', overwrite=False)
