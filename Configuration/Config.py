# -*- coding: utf-8 -*-
"""
Configuration for the pre and post processing is stored here. This includes
the channels which are to be analyised, and from those channels, the channels
which require frequency analysis, and the channels which require equivalent
load calculations.
@author: J
"""

class Config(object):
    # modelpath: the directory which contains the HAWC2 turbine model as well
    # as the results of the simulations.
    modelpath = 'C:/JL0004/'

    # manifestpath: the directory which contains the manifest .csv files.
    # The manifests contain a list of all simulations and parameters in a DLC.
    # It is the linking file between preprocessing and post processing.
    # !!! Assumes current directory is only one folder deep.
    manifestpath = '../Manifests/'

    # masterpath: the directory which contains the master .htc files from which
    # to generate the DLC .htc files.
    masterpath = manifestpath

    # channels: the channels in the HAWC2 result file which are to be loaded.
    # the keys are the label which will be used to access the data, and the
    # value is the channel number in the result file.
    channels = {
                't'         : 1,    #time [s]
                'wsp'       : 15,   #wind speed [m/s]
                'Paero'     : 12,   #aerodynamic power [?]
                'Pelec'     :103,   #electrical power [W]
                'Azim'      :  2,   #rotor azimuth angle [deg]
                'RBM1'      : 26,   #flapwise root bending moment - blade 1 [kNm]
                'RBM2'      : 29,
                'RBM3'      : 32,
                'RBMe1'     : 27,  #edgewise root bending moment [kNm]
                'RBMe2'     : 30,
                'RBMe3'     : 33,
                'RBMt1'     : 28,  #torsional root bending moment [kNm]
                'RBMt2'     : 31,
                'RBMt3'     : 34,
                'MBx'       : 112,#23, #Main bearing moment [kNm]
                'MBy'       : 114,#24,
                'MBz'       : 113,#25,
                'MTBx'      : 17, #Tower base moment [kNm]
                'MTBy'      : 18,
                'TD1'       : 49,   #Tip deflection - blade 1 [m]
                'TD2'       : 52,
                'TD3'       : 55,
                'pitch1'    :  4,   #pitch angle blade 1 [deg]
                'pitch2'    :  6,
                'pitch3'    :  8,
                'pitchrate1':  5,  # Pitch rate blade 1 [deg/s]
                'pitchrate2':  7,
                'pitchrate3':  9,
                'PPDem1'    : 71,   #Power pitch demand - blade 1 [?]
                'PPDem2'    : 72,
                'PPDem3'    : 73,
                'IPCDem1'   : 99,   #IPC pitch demand - blade 1 [rad]
                'IPCDem2'   : 100,
                'IPCDem3'   : 101,
                'status'    : 91,  # Turbine status <=0 okay, >0 shutdown}
                'tcl'       : 111} # Tower clearance

    # freqCh: the names of the channels which are to be frequency analysed.
    freqCh = ['PPDem1','pitch1','RBM1','RBMe1','RBMt1','MBx','MBy','MBz',
               'MTBx','MTBy','TD1','Pelec', 'Azim']

    # The maximum frequency to be considered for the frequency analysis.
    fmax = 0.7    #[Hz]
    # wohler: the names and the corresponding wohler constant of the channels
    # which are to be fatigue load tested.
    wohler = {
    'MBx': 4,
    'MBy': 4,
    'MBz': 4,
    'MTBx': 4,
    'MTBy': 4,
    'RBM1': 10,
    'RBM2': 10,
    'RBM3': 10,
    'RBMe1': 10,
    'RBMe2': 10,
    'RBMe3': 10,
    'RBMt1': 10,
    'RBMt2': 10,
    'RBMt3': 10}

