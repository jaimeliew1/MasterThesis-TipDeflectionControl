# -*- coding: utf-8 -*-
"""
A demonstration file for DLC preprocessing python script. Includes detailed
descriptions of each of the required parameters as well as an example of typical
parameters used in a dlc.
"""

from JaimesThesisModule import PreProc

# DLC parameters

# The basename is used as the directory for most files used in the dlc, as well.
# The basename is used to refer to this dlc in the pre and post processing, so
# name it thoughtfully.
basename = 'dlc_template'

# filename_func is a function which takes a dictionary of parameters (p) and is
# used to generate the filename of the simulation files. Here is an example
# filename function which generates filenames of the form:
# dlc_template_{yaw}_{wsp}_{seed}
fn_ = basename + '_{:03d}_{:02d}_{}'
def filename_func(p):
    return fn_.format(p['yaw'],
                      p['wsp'],
                      p['seed'])

# Constants are parameters which are the same for all simulations. For example,
# the duration of the simulation, or the result and log directories. The
# values of the Constants dictionary should be numbers (int, float), strings,
# or similar non-iterable types.
Constants = {'Tstart'   :   100,
             'Tstop'    :   700,
             'Nx'       :   8192,
             'logfolder':   './log/dlc11_0/',
             'resfolder':   './res/dlc11_0/',
                 }

# Variables are parameters which are changed in each simulation, for example,
# the wind speed or the seed. One simulation for every combination of
# variable parameters is generated. The values of the Variable dictionary should
# a list of values(or some kind of iterable).
Variables = {
             'yaw'          : [0],
             'wsp'          : [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
             '_seed'        : [1, 2]}

# Functionals are parameters which depend on constant and variable parameters.
# The values of the Functionals dictionary should be functions which take
# a dictionary as an input, and output the value or string to be substituted in
# the master .htc file. The input dictionary contains the Constants and Variables of the particular simulation.
Functionals = {'seed'       : lambda x: 1000*x['_seed'] + x['wsp'],
              'Tint'        : lambda x: (0.75*x['wsp'] + 5.6)*0.16/x['wsp'],
              'dx'          : lambda x: x['wsp'] * x['Tstop'] / x['Nx'],
              'filename'    : filename_func}

#%% Preprocessing
manifest = PreProc.Manifest(basename, Constants, Variables, Functionals)

manifest.checkTemplate('../Manifests/Master.htc')
manifest.missingRes()
#manifest.save_csv(basename + '.csv')
#!!! if manifest.template_valid('Master.htc'):
#!!!    manifest.generate(manifest=True, htc=True, pbs=True, mode='unrun') #or 'missing', or 'all'