# -*- coding: utf-8 -*-
"""
First prototype of a pythonic class for a HAWC2 DLC
@author: Jaime Liew
"""
import os
import numpy as np
import pandas as pd
from scipy import signal
from JaimesThesisModule.Misc import readHawc2Res
#from Misc import readHawc2Res
class DesignLoadCase(object):

    ModelDir = 'DTU10MW_Turbine/'
    def __init__(self, fn, modelDir='DTU10MW_Turbine/', loadAll=False):
        if fn[-4:].lower() != '.csv':
            fn = fn + '.csv'
        if not os.path.isfile(fn):
            raise FileNotFoundError('Parameter file {} does not exist.'.format(fn))
        self.params = pd.DataFrame.from_csv(fn, index_col=None)

        self.name = fn.split('.')[0]
        self.setModelDir(modelDir)


        if loadAll:
            pass
            #self.loadResults(ch=None,)
    def __repr__(self):
        return self.name.split('.')[0]

    def setModelDir(self,modelDir):
        if modelDir[-1] != '/':
            modelDir = modelDir + '/'

        self.ModelDir = modelDir
        self.HTCDir = modelDir + 'htc/' + self.name + '/'
        self.LogDir = modelDir + 'log/' + self.name + '/'
        self.ResDir = modelDir + 'res/' + self.name + '/'

    def missingHTC(self):
        # Returns list of missing HTC files in turbine model directory.
        missingFiles = []
        for f in self.params.filename:
            if not os.path.isfile(self.HTCDir + f + '.htc'):
                missingFiles.append(f)
        return missingFiles

    def missingResults(self):
        # Returns list of missing result files in turbine model directory.
        missingFiles = []
        for f in self.params.filename:
            if not os.path.isfile(self.ResDir + f + '.sel'):
                missingFiles.append(f)
        return missingFiles

    def missingLogs(self):
        # Returns list of missing log files in turbine model directory.
        missingFiles = []
        for fn in self.params.filename:
            if not os.path.isfile(self.LogDir + fn + '.log'):
                missingFiles.append(fn)
        return missingFiles

    def checkTemplateValidity(self, template_file):
        with open(template_file) as f:
            data = f.read()
        temp_params = [x.split('}')[0] for x in data.split('{')[1:]]
        undefParams = [x for x in temp_params if x not in self.params.keys()]
        overdefParams = [x for x in self.params.keys() if x not in temp_params]

        if undefParams:
            print('Undefined template parameters:')
            print(undefParams)
        if overdefParams:
            print('Defined parameters not in template file:')
            print(overdefParams)

        if not any([undefParams, overdefParams]):
            print('All parameters defined')
            return True
        else:
            return False


        #[x in TemplateAttr for x in params.keys()]

    def writeHTC(self, template_fn, dest=None, overwrite=False):
        # generates htc files using a template htc file located at template_fn.
        # uses parameters from self.params. if no destination folder is provided,
        # the files are written in self.HTCDir. If overwrite is False, only
        # htc files which do not exist will be written. Otherwise, all files will
        # be written.

        # error check
        if not os.path.isfile(template_fn):
            raise FileNotFoundError('Template file {} does not exist.'.format(template_fn))
        if dest is None:
            dest = self.HTCDir
        if not os.path.exists(dest):
            os.makedirs(dest)

        with open(template_fn) as f:
            TemplateText = f.read()

        for _, paramset in self.params.iterrows():
            FileText = TemplateText
            if not overwrite:
                if os.path.exists(dest + paramset.filename + '.htc'):
                    continue
            for key, value in paramset.items():
                FileText = FileText.replace('{' + key + '}', str(value))
                with open(dest + paramset.filename + '.htc', 'w') as f:
                    f.write(FileText)
                print('{}.htc created.'.format(paramset.filename))

    def writeBAT(self, filename, mask=None, exe='HAWC2MB.exe', incomplete=False):
        #TODO take out the mask and add something more useful
        if mask is None:
            mask = [True] * len(self.params)
        if incomplete:
            fns = self.missingResults()
            with open(self.ModelDir + filename, 'w') as f:
                for fn in fns:
                    f.write(exe + ' htc/{}.htc\n'.format(fn))
        else:
            with open(self.ModelDir + filename, 'w') as f:
                for fn in self.params.filename[mask]:
                    f.write(exe + ' htc/{}.htc\n'.format(fn))

    def ParamsComplete(self):
        # Returns dataframe of file parameters for only completed simulations.
        # Completeless is determined by analysing the log files, not the result
        # files.
        complete = np.zeros(len(self.params), dtype=bool)
        for i, fn in enumerate(self.params.filename):
            if os.path.isfile(self.LogDir + fn + '.log'):
                with open(self.LogDir + fn + '.log') as f:
                    if 'Elapsed time' in f.readlines()[-1]:
                        complete[i] = True

        paramsComplete = self.params[complete]
        paramsComplete = paramsComplete.reset_index(drop=True)
        return paramsComplete

    def loadResults(self, ch=None, freqCh=None, fmax=None, nperseg=4096):
        self.Data = []
        paramsComplete = self.ParamsComplete()

        if ch is None:
            print('This needs to be done')
        if ch is not None:

            for fn in paramsComplete.filename:
                d = readHawc2Res(self.ResDir + fn, channels=ch)
                self.Data.append(d)

    def ParamsComplete2(self):
        # Returns dataframe of file parameters for only completed simulations.
        # Assumes all results files are complete
        complete = np.zeros(len(self.params), dtype=bool)
        for i, fn in enumerate(self.params.filename):
            if os.path.isfile(self.ResDir + fn + '.sel'):
                complete[i] = True

        paramsComplete = self.params[complete]
        paramsComplete = paramsComplete.reset_index(drop=True)
        return paramsComplete

    def loadResults2(self, ch=None, freqCh=None, fmax=None, nperseg=4096):
        self.Data = []
        paramsComplete = self.ParamsComplete2()

        if ch is None:
            print('This needs to be done')
        if ch is not None:

            for fn in paramsComplete.filename:
                d = readHawc2Res(self.ResDir + fn, channels=ch)
                self.Data.append(d)

        #Frequency domain results
        self.Data_f = []
        self.Fs = 1/0.025 # Sampling frequency [hz], AUTOMATICALLY DETERMINE THIS
        if fmax is None:
            fmax = self.Fs/2 # Nyquist frequency

        if freqCh is None:
            pass #TODO
        if freqCh == 'all':
            for d in self.Data:
                data = dict()
                for key in self.Data[0].keys():
                    f, resp = signal.welch(d[key],self.Fs,nperseg=nperseg)
                    data[key] = resp[f < fmax]
                data['f'] = f[f < fmax]
                self.Data_f.append(pd.DataFrame(data))

        if isinstance(freqCh, list):
            for d in self.Data:
                data = dict()
                for key in freqCh:
                    f, resp = signal.welch(d[key],self.Fs,nperseg=nperseg)
                    data[key] = resp[f < fmax]
                data['f'] = f[f < fmax]
                self.Data_f.append(pd.DataFrame(data))

        self.Sims = paramsComplete
        return paramsComplete

    def formatParams(self, attributes):
        self.Sims = self.Sims[attributes]

    def getParams(self, complete=True, **kwargs):
        # returns the parameters of the DLC simulations subject to the filter
        #defined by kwargs. If complete==True, returns parameters from only
        # completed simulations.
        # example. dlc.getParams(wsp=[12, 14], controller='noIPC')
        # returns parameters in pandas DataFrame.
        if complete is not True:
            pass #TODO

        mask = [True] * len(self.Sims)
        for key, value in kwargs.items():
            if isinstance(value,(list, tuple, np.ndarray)):
                mask_temp = [False] * len(self.Sims)
                for v in value:
                    mask_temp = mask_temp | (self.Sims[key] == v)
                mask = mask & mask_temp
            else: #scalar, or single value
                mask = mask  & (self.Sims[key] == value)
        return self.Sims[mask]

    def getData(self, freq=False, **kwargs):
        # returns a list of simulation data subject to the filter defined by
        # kwargs. if freq==True, returns frequency data. Otherwise, returns
        # time series data.
        # returns results as a list of Pandas DataFrames
        filtered = self.getParams(**kwargs)
        out = []
        for ind, refSim in filtered.iterrows():
            if freq:
                out.append(self.Data_f[ind])
            else:
                out.append(self.Data[ind])
        return out

    def itersims(self, freq=False, **kwargs):
        filtered = self.getParams(**kwargs)
        for ind, refSim in filtered.iterrows():
            if freq:
                yield refSim, self.Data_f[ind]
            else:
                yield refSim, self.Data[ind]

    def unique(self, att, **kwargs):
        filtered = self.getParams(**kwargs)
        return filtered[att].drop_duplicates()




if __name__ == '__main__':
    channels = {
                't'         : 1,    #time [s]
                'wsp'       : 15,   #wind speed [m/s]
                'Paero'     : 12,   #aerodynamic power [?]
                'Pelec'     :100,   #electrical power [W]
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
                'MBx'       : 23, #Main bearing moment [kNm]
                'MBy'       : 24,
                'MBz'       : 25,
                'MTBx'      : 17, #Tower base moment [kNm]
                'MTBy'      : 18,
                'TD1'       : 49,   #Tip deflection - blade 1 [m]
                'TD2'       : 52,
                'TD3'       : 55,
                'pitch1'    :  4,   #pitch angle blade 1 [deg]
                'pitch2'    :  6,
                'pitch3'    :  8,
                'PPDem1'    : 71,   #Power pitch demand - blade 1 [?]
                'PPDem2'    : 72,
                'PPDem3'    : 73,
                'IPCDem1'   : 99,   #IPC pitch demand - blade 1 [rad]
                'IPCDem2'   : 100,
                'IPCDem3'   : 101}
    freqCh = ['PPDem1','pitch1','RBM1','RBMe1','RBMt1','MBx','MBy','MBz',
               'MTBx','MTBy','TD1','Pelec', 'Azim']

    dlc = DesignLoadCase('../ReducedCase_1.csv',modelDir='../DTU10MW_Turbine')

    #dlc2 = DesignLoadCase('DLC11_Parameters.csv')
    #dlc2.checkTemplateValidity('template/Master.htc')
    #dlc2.writeHTC('template/Master.htc', dest='DLC11/', overwrite=False)
    print(dlc.missingResults())
    dlc.loadResults(channels, freqCh, fmax=0.7)
    dlc.formatParams(['wsp','controller','Kp','seed'])


    for a,b in dlc.itersims(freq=True,wsp=12):
        print(a)

    #mask = dlc2.params.filename == 'DLC11_IPC1p_025_12_1012'
    #dlc2.writeBAT('TEST.bat',mask=mask)
#from DesignLoadCase import DesignLoadCase
#fn_struc = 'FILENAME_CONTROLFILE_WSP_Kp_SEED'
#DLC = DesignLoadCase('dlcDefinitionFile.csv', fn_struc, loadAll=False)
#

#DLC.missingHTC()
#DLC.missingResults()
#DLC.writeHTC(overwrite=False)
#
#data_t, data_f = DLC.loadResults(ch=None, freqCh=None, fMax=None, nperseg=1024*4)
#DLC.setWoller(ListofWollerConstants)
#Req = DLC.Req()
#Req = DLC.Req(ListofWollerConstants)
#stats = DLC.stats(listOfIndices)
#paramsDataFrame = DLC.Params(complete=True)
#
#data = DLC.Data
#
#for param, data in DLC.itersim(mask):
#    pass
#DLC2 = DesignLoadCase('anotherDLCDefinition.csv')

