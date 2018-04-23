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
from scipy import signal



# TODO Implement Configuration.Config more neatly through out post processing


class Seed(object):
    def __init__(self, i, df=None):
        self.ind = i
        if df is not None:
            self.filename = df.filename
            self.wsp = df.wsp
            self.controller = df.controller
            self.Kp = df.Kp
            self.seed = df.seed
            self.yaw = df.yaw
        else:
            self.filename = None
            self.wsp = None
            self.controller = None
            self.Kp = None
            self.seed = None
        self.Data = None
        self.fData = None
        self.Req = None
        self.shutdown = None
        self.max = None
        self.min = None
        self.mean = None
        self.std = None
        self.pitchtravel = None


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

    def loadFromSel(self, resFolder, channels=None):
        self.Data = readHawc2Res(resFolder + self.filename, channels=channels)

    def load(self, resFolder, light=False):
        f = np.load(resFolder + self.filename + '.npz')
        self.fData = pd.DataFrame(f['fData'], columns=f['fDataLab'])
        self.Req = pd.DataFrame(f['Req'], columns=f['ReqLab'])
        self.shutdown = f['shutdown']
        self.mean = pd.DataFrame(np.reshape(f['mean'], [1,-1]), columns=f['DataLab'])
        self.std = pd.DataFrame(np.reshape(f['std'], [1,-1]), columns=f['DataLab'])
        self.max = pd.DataFrame(np.reshape(f['max'], [1,-1]), columns=f['DataLab'])
        self.min = pd.DataFrame(np.reshape(f['min'], [1,-1]), columns=f['DataLab'])
        self.pitchtravel = f['pitchtravel']
        if not light:
            self.Data = pd.DataFrame(f['Data'], columns=f['DataLab'])

    def save(self, resFolder):
        toSave = {'Data'    : self.Data,
                  'DataLab' : self.Data.keys(),
                  'fData'   : self.fData,
                  'fDataLab': self.fData.keys(),
                  'Req'     : self.Req,
                  'ReqLab'  : self.Req.keys(),
                  'shutdown': self.shutdown,
                  'mean'    : self.mean,
                  'std'     : self.std,
                  'max'     : self.max,
                  'min'     : self.min,
                  'pitchtravel': self.pitchtravel}

        np.savez_compressed(resFolder + self.filename + '.npz', **toSave)

    def analysis(self, freqCh=None, fmax=None, wohler=None, nperseg=4096):
        if self.Data is None:
            print('No Data loaded')
            return -1


        # Frequency response analysis
        self.Fs = 1/0.01 # Sampling frequency [hz], AUTOMATICALLY DETERMINE THIS
        if fmax is None:
            fmax = self.Fs/2 # Nyquist frequency
        if freqCh is None:
            freqCh = self.Data.keys()


        temp = dict()
        for key in freqCh:
            f, resp = signal.welch(self.Data[key], self.Fs, nperseg=nperseg)
            temp[key] = resp[f < fmax]
        temp['f'] = f[f < fmax]
        self.fData = pd.DataFrame(temp)

        #Shutdown analysis
        if any(self.Data.status > 0):
            self.shutdown = 1
        else:
            self.shutdown = 0


        #statistical analysis
        if not self.shutdown:
            self.mean = self.Data.mean()
            self.max = self.Data.max()
            self.min = self.Data.min()
            self.std = self.Data.std()
        else:
            allnans = [np.full(len(self.Data.keys()), np.nan)]
            self.mean = pd.DataFrame(allnans, columns = self.Data.keys())
            self.max = pd.DataFrame(allnans, columns = self.Data.keys())
            self.min = pd.DataFrame(allnans, columns = self.Data.keys())
            self.std = pd.DataFrame(allnans, columns = self.Data.keys())

        #Equivalent load analysis.
        if wohler is not None:


            self.Req = np.zeros(len(wohler.keys()))
            for i, (channel, woh) in enumerate(wohler.items()):
                if self.shutdown == 1:
                    self.Req[i] = np.nan
                else:
                    self.Req[i], _, _ = EquivalentLoad(self.Data[channel], 600, woh)

            self.Req = pd.DataFrame(np.reshape(self.Req, [1, -1]), columns=wohler.keys())

        # Pitch Travel analysis
        self.pitchtravel = [np.trapz(abs(self.Data['pitchrate' + str(i)]), self.Data.t) for i in [1,2,3]]
        self.pitchtravel = np.mean(self.pitchtravel)





class Simulation(object):
    def __init__(self, i, df=None, seeds=None):
        self.ind = i
        if df is not None:
            self.wsp = df.wsp
            self.controller = df.controller
            self.Kp = df.Kp
            self.yaw = df.yaw
        else:
            self.wsp = None
            self.controller = None
            self.Kp = None
            self.yaw = None
        self.fData = None
        self.Req = None
        self.shutdown = None
        self.pitchtravel = None
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

    def loadFromSel(self, resFolder, channels=None):
        for seed in self.seeds:
            seed.loadFromSel(resFolder, channels=channels)

    def save(self, resFolder):
        for seed in self.seeds:
            seed.save(resFolder)

    def load(self, resFolder, light=False):
        for seed in self.seeds:
            seed.load(resFolder, light=light)


    def analysis(self, freqCh=None, fmax=None, wohler=None, nperseg=4096, resfolder=None):
        N = len(self.seeds)

        for i, seed in enumerate(self.seeds):
            seed.analysis(freqCh, fmax, wohler, resfolder=resfolder)

            if i == 0:
                self.fData =seed.fData/N
                self.Req = seed.Req/N
                self.shutdown = seed.shutdown/N
                self.mean = seed.mean/N
                self.std = seed.std/np.sqrt(N) #!!! Double check this
                self.max = seed.max
                self.min = seed.min
                self.pitchtravel = seed.pitchtravel/N
            else:
                self.fData += seed.fData/N
                self.Req += seed.Req/N
                self.shutdown += seed.shutdown/N
                self.mean += seed.mean/N
                self.std = seed.std/np.sqrt(N) #!!! double check this
                self.max = np.maximum(self.max, seed.max)
                self.min = np.minimum(self.min, seed.min)
                self.pitchtravel += seed.pitchtravel/N

    def simAnalysis(self):
        N = len(self.seeds)
        for i, seed in enumerate(self.seeds):

            if i == 0:
                self.fData =seed.fData/N
                self.Req = seed.Req/N
                self.shutdown = seed.shutdown/N
                self.mean = seed.mean/N
                self.std = seed.std/np.sqrt(N) #!!! Double check this
                self.max = seed.max
                self.min = seed.min
                self.pitchtravel = seed.pitchtravel/N
            else:
                self.fData += seed.fData/N
                self.Req += seed.Req/N
                self.shutdown += seed.shutdown/N
                self.mean += seed.mean/N
                self.std = seed.std/np.sqrt(N) #!!! double check this
                self.max = np.maximum(self.max, seed.max)
                self.min = np.minimum(self.min, seed.min)
                self.pitchtravel += seed.pitchtravel/N









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

        for i, row in self.seedParams.iterrows():
            self.seeds.append(Seed(i, row))

        for seed in self.missingResults():
            print('{} is missing.'.format(seed))
            #self.seeds.remove(self.seeds[seed.ind])
            self.seeds.remove(seed)
        self.consolidateSimulations()

    #def __iter__(self):
        #return iter(self.Sims)#
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

    def loadResults(self, ch=None):
        resfolder = Config.modelpath + 'res/' + self.basename + '/'

        if ch is None:
            print('This needs to be done') #TODO
        if ch is not None:
            for sim in self.Sims:
                sim.loadFromSel(resfolder, ch)


    def consolidateSimulations(self, unique= ['wsp', 'controller', 'Kp', 'yaw']):
        self.params = self.seedParams[unique].drop_duplicates()
        for i, p in self.params.iterrows():
            kwargs = {}
            for key in unique:
                kwargs[key] = p[key]

            seeds = [x for x in self.seeds if x.match(p)]

            self.Sims.append(Simulation(i, p, seeds=seeds))




    def analysis(self, mode='fullload', settings=None, PRINT=True):
        # perform frequency, equivalent load etc analysis. if mode is 'fullload',
        # all data and analysis data is loaded from file if it exists. otherwise,
        # analysis is performed and saved. if mode is 'lightload', only analysis data
        # is loaded. otherwise, analysis is performed and saved. if modeis 'do',
        # the analysis and loading is done regardless of if files exist.

        #Get analysis parameters from config file

        resFolder = Config.modelpath + 'res/' + self.basename + '/'
        for i, seed in enumerate(self.seeds):
            if PRINT:
                print('\rAnalysing: {}/{}'.format(i, len(self.seeds)), end='')
            if mode == 'do':# slow
                seed.loadFromSel(resFolder, Config.channels)
                seed.analysis(Config.freqCh, Config.fmax, Config.wohler)
            elif mode == 'dosave':# slowest
                seed.loadFromSel(resFolder, Config.ch)
                seed.analysis(Config.freqCh, Config.fmax, Config.wohler)
                seed.save(resFolder)
            elif mode == 'fullload':# fast
                if os.path.isfile(resFolder + seed.filename + '.npz'):
                    seed.load(resFolder)
                else:
                    seed.loadFromSel(resFolder, Config.channels)
                    seed.analysis(Config.freqCh, Config.fmax, Config.wohler)
                    seed.save(resFolder)
            elif mode =='lightload': # fastest
                if os.path.isfile(resFolder + seed.filename + '.npz'):
                    seed.load(resFolder, light=True)
                else:
                    seed.loadFromSel(resFolder, ch)
                    seed.analysis(Config.freqCh, Config.fmax, Config.wohler)
                    seed.save(resFolder)

        for sim in self.Sims:
            sim.simAnalysis()

        if PRINT:
            print()


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

