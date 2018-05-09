# -*- coding: utf-8 -*-
"""
Modified DLC1.5 for DTU10MW turbine with inverse shear and no IPC. Mirrors
the simulations in DLC11_0.
"""

from JaimesThesisModule import PreProc

# DLC parameters.

basename = 'dlc15_0'

fn_ = basename + '_{}_{:02d}_{}'
fn_func = lambda x: fn_.format(x['controller'], x['wsp'], x['seed'])

Constants = {'Tstart'   :   100,
             'Tstop'    :   700,
             'Nx'       :   8192,
             'logfolder':   './log/dlc15_0/',
             'resfolder':   './res/dlc15_0/',
             'controller': 'noipc',
             'yaw'      : 0,
             'Kp'       : 0}

Variables = {
             'wsp'          : [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
             '_seed'        : [1, 2, 3]}


Functionals = {'seed'       : lambda x: 1000*x['_seed'] + x['wsp'],
              'Tint'        : lambda x: (0.75*x['wsp'] + 5.6)*0.16/x['wsp'],
              'dx'          : lambda x: x['wsp'] * x['Tstop'] / x['Nx'],
              'filename'    : fn_func}

#%% Preprocessing
manifest = PreProc.Manifest(basename, Constants, Variables, Functionals)
manifest.printOverview()

manifest.checkTemplate('../Manifests/Master_InverseShear.htc')
manifest.missingRes()
manifest.save_csv()
manifest.generate_htc_files('../Manifests/Master_InverseShear.htc', overwrite=False)
