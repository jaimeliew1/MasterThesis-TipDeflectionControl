# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:00:36 2018

@author: J
"""
from scipy import interpolate
import numpy as np

directory = '../Modelling/Data/'


def Response(wsp, rad=False):
    # returns the frequency magnitude response function of the tip
    # deflection at windspeed = wsp as a function of frequency in
    # Hertz. If rad=True, then frequency is in rad/s
    filename = 'OLResponse_{}.csv'.format(wsp)
    data = np.loadtxt(directory + filename)
    f = data[0, :]
    Y = data[1, :]

    if rad:
        f = f*2*np.pi

    Yol = interpolate.interp1d(f, Y, kind='cubic', bounds_error=False)

    return Yol


if __name__ == '__main__':
    directory =  'Data/'


