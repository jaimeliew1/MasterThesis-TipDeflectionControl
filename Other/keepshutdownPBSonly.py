# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 16:32:01 2018

@author: J
"""
import os
from JaimesThesisModule import PostProc

basename = 'dlc11_3'
pbsindir = 'C:/JL0004/pbs_in/'


dlc = PostProc.DLC(basename)
filenames = os.listdir(pbsindir + basename)
print(len(filenames))
assert len(dlc.seeds) == len(filenames)

for seed in dlc.seeds:
    if not seed.data.shutdown:
        #os.remove(pbsindir + basename + '/' + seed.filename + '.p')
        #print(seed.filename, '.p deleted.')
        pass
