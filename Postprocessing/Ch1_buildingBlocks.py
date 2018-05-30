# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:43:36 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



def addLeadCompensator(self, lead, freq):
# Adds the pole and zero for lead compensation which adds 'lead'
# amount of phase [deg] at 'freq' [Hz]
    lead = lead * np.pi/180
    freq = freq * 2 *np.pi

    a = (1 + np.sin(lead))/(1 - np.sin(lead))
    T = 1/(np.sqrt(a) * freq)
    self.addPole(-1/T)
    self.addZero(-1/(a*T))