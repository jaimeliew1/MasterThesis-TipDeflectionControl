# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:16:14 2018

@author: J
"""
import numpy as np
import pandas as pd
import os
from Configuration.Config import Config
from wetb.hawc2.htc_file import HTCFile #!!! shouldnt rely on this package
from itertools import product

class ModelMissingException(Exception):
    pass

class Manifest(object):

    def __init__(self, *args):
        nargs = len(args)

        if nargs==1:
            raise NotImplementedError
            #self.from_csv(args[0])

        if nargs>=4:
            self.gen_manifest(*args)

    def __getitem__(self, arg):
        return self._man.iloc[arg]

    def __len__(self):
        return len(self._man)

    def from_csv(self, filename):
        self._man = pd.read_csv(filename)
        self.N = len(self._man)
        self.M = len(self._man.keys())

    def missingRes(self):
        try:
            filenames = os.listdir(Config.modelpath + 'res/' + self.basename)
        except FileNotFoundError:
            print('Result folder not found.')
            return
        filenames = [x[:-4] for x in filenames if '.sel' in x]
        n_missing = 0
        for f in self._man.filename:
            if f not in filenames:
                print(f)

    def gen_manifest(self,basename, Consts, Vars, Funcs, order=None):
        self.basename = basename
        # number of combinations:
        self.N = 1
        for n in [len(x) for x in Vars.values()]:
            self.N *= n
        # number of attributes:
        attributes = list(Consts.keys()) + list(Vars.keys()) + list(Funcs.keys())
        self.M = len(attributes)

        # generate a Pandas dataframe where each row has one of the combinations
        # of simulation parameters
        manifest = []
        for v in product(*list(Vars.values())):
            v_dict = dict(zip(Vars.keys(), v))
            this_dict = {**Consts, **v_dict}

            for key, f in Funcs.items():
                this_dict[key] = f(this_dict)

            manifest.append(list(this_dict.values()))

        self._man = pd.DataFrame(manifest, columns=attributes)

    def save_csv(self):
        self._man.to_csv(Config.manifestpath + self.basename + '.csv', index=False)

    def checkTemplate(self, filename=None):

        with open(filename) as f:
            data = f.read()
        temp_params = [x.split('}')[0] for x in data.split('{')[1:]]
        undefParams = [x for x in temp_params if x not in self._man.keys()]
        overdefParams = [x for x in self._man.keys() if x not in temp_params]

        # ignore attributes starting with _
        undefParams = [x for x in undefParams if x[0] is not '_']
        overdefParams = [x for x in overdefParams if x[0] is not '_']
        if undefParams:
            print('Parameters in template but not in manifest:')
            print(undefParams)
        if overdefParams:
            print('Parameters in manifest but not in template:')
            print(overdefParams)

        if not any([undefParams, overdefParams]):
            print('All template parameters defined')
            return True
        else:
            return False

    def printOverview(self):
        print('DLC contains {} HAWC2 simulations'.format(len(self)))

        print('The first 5 simulation filenames are:')
        for i in range(5):
            print(self[i].filename)

        print('The last 5 simulation filenames are:')
        for i in range(5):
            print(self[-(i+1)].filename)




    def generate_htc_files(self, template_fn, overwrite=True):
        # generates htc files using a template htc file located at template_fn.
        # uses parameters from self.params. if no destination folder is provided,
        # the files are written in self.HTCDir. If overwrite is False, only
        # htc files which do not exist will be written. Otherwise, all files will
        # be written.

        # error check
        if not os.path.isfile(template_fn):
            raise FileNotFoundError('Template file {} does not exist.'.format(template_fn))

        dest = Config.modelpath + 'htc/' + self.basename + '/'

        if not os.path.exists(dest):
            os.makedirs(dest)

        with open(template_fn) as f:
            TemplateText = f.read()

        for _, paramset in self._man.iterrows():
            FileText = TemplateText
            if not overwrite:
                if os.path.exists(dest + paramset.filename + '.htc'):
                    continue
            for key, value in paramset.items():
                if key[0] is '_':
                    continue
                FileText = FileText.replace('{' + key + '}', str(value))
                with open(dest + paramset.filename + '.htc', 'w') as f:
                    f.write(FileText)
                print('{}.htc created.'.format(paramset.filename))

    def generate_pbs_files(self, template_fn, overwrite=True):
        with open(template_fn) as f:
            template = f.read()

        p = {
                        'walltime'      : '00:40:00',
                        'umask'         : '003',
                        'lnodes'        : '1',
                        'ppn'           : '1',
                        'modelzip'      : 'JL0001.zip',
                        'jobname'       : 'ERROR',
                        'htcdir'        : 'ERROR',                #from htc file
                        'logdir'        : 'ERROR',
                        'resdir'        : 'ERROR',
                        'turbdir'       : 'ERROR',
                        'turbfileroot'  : 'ERROR'}              #from htc file


        pbs_in_dir = Config.modelpath + 'pbs_in/' + self.basename
        htc_dir = Config.modelpath + 'htc/' + self.basename

        #if not, check if zip files exist. if more than one, return error
        zipfiles = [x for x in os.listdir(self.modelpath) if '.zip' in x]

        if len(zipfiles) == 0:
            raise ModelMissingException('No zipped model file found in this folder.')
        elif len(zipfiles) > 1:
            raise ModelMissingException('Only one zipped model file should be supplied in this folder.')
        #set zip file
        p['modelzip'] = zipfiles[0]



        if not os.path.exists(pbs_in_dir):
            os.makedirs(pbs_in_dir)

        filenames = [x for x in os.listdir(htc_dir) if x[-4:] == '.htc']
        for file in filenames:
            htc = HTCFile(os.path.join(htc_dir, file), modelpath='../..')

            p['jobname'] = file.split('.')[0]
            p['htcdir'] = 'htc/' + basename
            p['logdir'] = os.path.dirname(htc.simulation.logfile.str_values())[2:] + '/'
            p['resdir'] = os.path.dirname(htc.output.filename.str_values())[2:] + '/'
            p['turbdir'] = os.path.dirname(htc.wind.mann.filename_u.str_values()) + '/'
            p['turbfileroot'] = os.path.basename(htc.wind.mann.filename_u.str_values()).split('u.')[0]
            p['pbsoutdir'] = 'pbs_out/' + basename
            template_ = template
            for key, value in p.items():
                template_ = template_.replace('[' + key + ']', value)

            with open(os.path.join(pbs_in_dir, file[:-4] + '.p'), 'w') as f:
                f.write(template_)
                print('{}.p created.'.format(file[:-4]))



if __name__ == '__main__':
    pass
