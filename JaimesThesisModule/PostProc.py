# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 17:25:20 2018
Defines the three base classes for performing post processing on design load
cases from HAWC2 results.

Seed:
----
An object which links to a single seed of a simulation of a DLC.

Simulation:
----------
An object which links to all the seeds of a single simulation.

DLC:
----
An object which links to all of the simulations of a design load case. The
simulations and seeds are defined in a manifest file (.csv) of the same basename
as the DLC.

@author: J
"""
import os
import numpy as np
import pandas as pd
import itertools
from Configuration.Config import Config
from JaimesThesisModule.Misc import readHawc2Res, EquivalentLoad
from scipy import signal, interpolate
import matplotlib.pyplot as plt

a = None

# TODO Implement Configuration.Config more neatly through out post processing


class Seed(object):
    def __init__(self, i, resFolder, df=None):
        self.ind = i
        self.resFolder = resFolder
        self.data = None
        if df is not None:
            self.filename = df.filename
            self.wsp = df.wsp
            self.controller = df.controller
            self.Kp = df.Kp
            self.seed = df.seed
            self.yaw = df.yaw
            a = df.index
            if '_amp' in df.index:

                self._amp = df['_amp']
                self.amp = self._amp

        else:
            self.filename = None
            self.wsp = None
            self.controller = None
            self.Kp = None
            self.seed = None



    def __repr__(self):
        return('Seed {}: {}'.format(self.ind, self.filename))

    def __eq__(self, other):
        if self.filename == other.filename:
            return True
        else:
            return False

    def match(self, df):
        # used for consolidating seeds into simulation groups
        if all([getattr(self, key) == df[key] for key in df.keys()]):
            return True
        else:
            return False

    def loadFromSel(self, channels=None):
        return readHawc2Res(self.resFolder + self.filename, channels=channels)


    def analysis(self, freqCh=None, fmax=None, wohler=None, nperseg=4096):
        self.data = np.zeros(11)
        Data = self.loadFromSel(Config.channels)


        # Equivalent load analysis.
        wohler = {
    'MBx': 4,'MBy': 4,'MBz': 4,'RBM1': 10,'RBM2': 10,'RBM3': 10,'RBMe1': 10,
    'RBMe2': 10,'RBMe3': 10,'RBMt1': 10,'RBMt2': 10,'RBMt3': 10}

        Req = np.zeros(len(wohler.keys()))
        for i, (channel, woh) in enumerate(wohler.items()):
            Req[i], _, _ = EquivalentLoad(Data[channel], 600, woh)

        Req = dict(zip(wohler.keys(), Req))

        # flapwise moment (RBMf)
        root = 'RBM'; ind = 0
        keys = [root + str(x) for x in [1, 2, 3]]
        temp = sum(1/3*Req[key]**wohler[key] for key in keys)
        self.data[ind] = temp**(1/wohler[keys[0]])

        # edgewise moment (RBMe)
        root = 'RBMe'; ind = 1
        keys = [root + str(x) for x in [1, 2, 3]]
        temp = sum(1/3*Req[key]**wohler[key] for key in keys)
        self.data[ind] = temp**(1/wohler[keys[0]])

        # torsion  moment (RBMt)
        root = 'RBMt'; ind = 2
        keys = [root + str(x) for x in [1, 2, 3]]
        temp = sum(1/3*Req[key]**wohler[key] for key in keys)
        self.data[ind] = temp**(1/wohler[keys[0]])

        # Main bearing tilt moment (MBt)
        self.data[3] = Req['MBx']

        # Main bearing yaw moment (MBy)
        self.data[4] = Req['MBy']


        # Frequency response analysis
        Fs = 100
        Ys = []
        for blade in [1, 2, 3]:
            key = 'TD{}'.format(blade)
            f, Py = signal.welch(Data[key], Fs, nperseg=1024*8)
            Ys.append(np.sqrt(Fs*Py/60000))

        Yave = np.mean(Ys, axis=0)
        Yol = interpolate.interp1d(f, Yave, kind='linear',
                                   bounds_error=False)

        self.data[5:9] = Yol(0.16*np.array([1, 2, 3, 4]))


    #Shutdown analysis
        if any(Data.status > 0):
            self.data[9] = 1
        else:
            self.data[9] = 0


        # tower clearance analysis

        # Finds and lists the lower peaks (valleys) in a time series by
        # finding reversals. Only returns the values, not the index/time.
        peaks = []
        for i, x in enumerate(Data.tcl):
            if i == 0 or i == len(Data.tcl)-1:
                continue

            if (Data.tcl[i-1] > x) and (Data.tcl[i+1] > x):
                peaks.append(x)

        if self.data[9] == 1: # if shutdown
            self.data[10] = -1
        else:
            self.data[10] = min(peaks)


        columns = ['RBMf', 'RBMe', 'RBMt', 'MBt', 'MBy', 'A1p', 'A2p',
                   'A3p','A4p','shutdown','tcl']
        self.data = pd.Series(self.data, index=columns)


#        # Pitch Travel analysis
#        self.pitchtravel = [np.trapz(abs(self.Data['pitchrate' + str(i)]), self.Data.t) for i in [1,2,3]]
#        self.pitchtravel = np.mean(self.pitchtravel)





class Simulation(object):
    def __init__(self, i, df=None, seeds=None):
        self.ind = i
        self.data = None
        if df is not None:
            self.wsp = df.wsp
            self.controller = df.controller
            self.Kp = df.Kp
            self.yaw = df.yaw

            if '_amp' in df.index:
                self.amp = df._amp
        else:
            self.wsp = None
            self.controller = None
            self.Kp = None
            self.yaw = None
            self.amp = None
        self.seeds = []


        if seeds is not None:
            self.addSeeds(seeds)

    def __repr__(self):
        return('Simulation: {} wsp: {} cont: {} Kp: {} yaw: {}'.format(self.ind, self.wsp, self.controller, self.Kp, self.yaw))



    def __len__(self):
        return len(self.seeds)

    def __contains__(self, x):
        return any(item.filename == x for item in self.seeds)

    #def __iter__(self):
    #    return iter(self.seeds)
    def __getitem__(self, index):
        return self.seeds[index]



    def addSeeds(self, seeds):
        for seed in seeds:
            if seed.wsp != self.wsp:
                print('Wsp doesn''t match!')
            if seed.controller != self.controller:
                print('controller doesn''t match!')
            if seed.Kp != self.Kp:
                print('Kp doesn''t match!')
            self.seeds.append(seed)



    def analysis(self, freqCh=None, fmax=None, wohler=None, nperseg=4096, resfolder=None):


        N = len(self.seeds)

        self.data = dict()

        wohler = [10, 10, 10, 4, 4]


        if all(x.data.shutdown for x in self.seeds):
            for key in ['A1p', 'A2p','A3p','A4p','RBMf', 'RBMe', 'RBMt', 'MBt', 'MBy']:
                self.data[key] = 0
        else:
            self.data['tcl'] = min(seed.data['tcl'] for seed in self.seeds if not seed.data.shutdown)
            Nsd = len([x for x in self.seeds if not x.data.shutdown])
            # Req
            # for each channel (RBMf, RBMe, etc...)
            for i, key in enumerate(['RBMf', 'RBMe', 'RBMt', 'MBt', 'MBy']):
                temp = sum(1/Nsd*seed.data[key]**wohler[i] for seed in self.seeds if not seed.data.shutdown)
                self.data[key] = temp**(1/wohler[i])



            for key in ['A1p', 'A2p','A3p','A4p']:
                self.data[key] = np.mean([seed.data[key] for seed in self.seeds if seed.data.shutdown==0])

        self.data['shutdown'] = np.mean([seed.data.shutdown for seed in self.seeds])



        # if any seeds shutdown, then set all summary data values to zero
#        if any(x.data.shutdown for x in self.seeds):
#            for key in self.data.keys():
#                if key is not 'shutdown':
#                    self.data[key] = 0




        self.data = pd.Series(list(self.data.values()),
                              index = self.data.keys())








class DLC(object):
    def __init__(self, basename, modelpath=None, filename=None):
        if filename is None:
            filename = Config.manifestpath + basename + '.csv'



        if not os.path.isfile(filename):
            raise FileNotFoundError('Parameter file {} does not exist.'.format(filename))
        self.seedParams = pd.DataFrame.from_csv(filename, index_col=None)


        self.basename = basename
        self.Sims = []
        self.seeds = []

        resFolder = Config.modelpath + 'res/' + self.basename + '/'
        for i, row in self.seedParams.iterrows():
            self.seeds.append(Seed(i, resFolder, row))

        for seed in self.missingResults():
            print('{} is missing.'.format(seed))
            self.seeds.remove(seed)



        if basename == 'dlc11_3' or basename == 'dlc15_2':
            self.consolidateSimulations(unique=['wsp', 'controller', '_amp', 'Kp', 'yaw'])
        else:
            self.consolidateSimulations()
        self.analysis()



    def __getitem__(self, index):
        return self.Sims[index]




    def __call__(self, **kwargs):
        mask = self.mask(**kwargs)
        return [i for (i, v) in zip(self.Sims, mask) if v]



    def __len__(self):
        return len(self.Sims)



    def missingResults(self):
        # Returns list of Seed objects coresponding to
        # missing result files in turbine model directory.
        resfolder = Config.modelpath + 'res/' + self.basename + '/'
        missingSeeds = []
        for seed in self.seeds:
            if not os.path.isfile(resfolder + seed.filename + '.sel'):
                missingSeeds.append(seed)
        return missingSeeds



    def consolidateSimulations(self, unique= ['wsp', 'controller', 'Kp', 'yaw']):
        self.params = self.seedParams[unique].drop_duplicates()
        for i, p in self.params.iterrows():
            kwargs = {}
            for key in unique:
                kwargs[key] = p[key]

            seeds = [x for x in self.seeds if x.match(p)]

            self.Sims.append(Simulation(i, p, seeds=seeds))




    def analysis(self):

        summaryDataFile = Config.manifestpath + self.basename + '_data.csv'
        columns = ['RBMf', 'RBMe', 'RBMt', 'MBt', 'MBy', 'A1p', 'A2p',
                   'A3p','A4p','shutdown','tcl']
        # if summary datafile exists, read from it. Else, run analysis and
        # save a new summary datafile
        if os.path.isfile(summaryDataFile):
            filedata = np.loadtxt(summaryDataFile)
            for seed, line in zip(self.seeds, filedata):
                seed.data = pd.Series(line, index = columns)
        else:
            for seed in self.seeds:
                print('\r Analysing seed {}/{}'.format(seed.ind, len(self.seeds)), end='')
                seed.analysis()
            filedata = np.array([x.data for x in self.seeds])
            np.savetxt(summaryDataFile, filedata)



        for sim in self.Sims:
            sim.analysis()


    def _mask(self, df, **kwargs):

        '''
        Returns a mask for refering to a dataframe, or self.Data, or self.Data_f, etc.
        example. dlc.mask(wsp=[12, 14], controller='noIPC')
        '''
        N = len(df)
        mask = [True] * N
        for key, value in kwargs.items():
            if isinstance(value, (list, tuple, np.ndarray)):
                mask_temp = [False] * N
                for v in value:
                    mask_temp = mask_temp | (df[key] == v)
                mask = mask & mask_temp
            else: #scalar, or single value
                mask = mask & (df[key] == value)
        return mask

    def mask(self, **kwargs):
        return self._mask(self.params, **kwargs)



    def unique(self, attributes, **kwargs):
        uniques = []
        for att in attributes:
            uniques.append(set(getattr(x, att) for x in self))

        return list(itertools.product(*uniques))


if __name__ is '__main__':
    dlc = DLC('dlc15_2')

