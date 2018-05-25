# -*- coding: utf-8 -*-
"""
Created on Wed May 23 18:05:04 2018

@author: J
"""

import numpy as np
from numpy import pi, sin, cos
import matplotlib.pyplot as plt
from scipy import signal




def freqResp(x, Fs, fmax=None):
    f  = np.linspace(0, Fs, len(x))
    Y = 2*abs(np.fft.fft(x))/len(x)

    if fmax:
        Y = Y[f <= fmax]
        f = f[f <= fmax]
    return f, Y




def dq(X, Theta, deg=False):
    ''' Performs the coleman transformation.
    input
    ^^^^^
    x   : a list or array of 3 elements containing the quantity
        to transform
    theta : the azimuth angle of the transformation
    deg : if True, theta is treated as in degrees. else, radians.
    output
    ^^^^^^
    y   : a list or array of 3 elements (collective, tilt
          and yaw) containing the transformed quantities.
    '''
    if deg:
        Theta = Theta*pi/180

    N = len(Theta)
    assert len(X) == N
    Y = np.zeros([N, 3])
    for i, (x, theta) in enumerate(zip(X, Theta)):
        Y[i, 0] = sum(x)/3
        Y[i, 1] = 2/3*cos(theta)*x[0] + 2/3*cos(theta + 2*pi/3) * x[1] + 2/3*cos(theta + 4*pi/3) * x[2]
        Y[i, 2] = 2/3*sin(theta)*x[0] + 2/3*sin(theta + 2*pi/3) * x[1] + 2/3*sin(theta + 4*pi/3) * x[2]
    return Y

Fs = 1000 # hz
T = 10
t = np.linspace(0, T, Fs*T)

f = 1.2
azim = 2*pi*t

x = np.array([sin(f*2*pi*t), sin(f*2*pi*(t + 1/3)), sin(f*2*pi*(t + 2/3))]).T
y = dq(x, azim, deg=False)

f, x_ = freqResp(x[:,0], Fs)
_, y1 = freqResp(y[:,0], Fs)
_, y2 = freqResp(y[:,1], Fs)
_, y3 = freqResp(y[:,2], Fs)


plt.figure()
plt.plot(t, x)
plt.xlim(0,1)

plt.figure()
plt.xlim(0,1)
plt.plot(t, y)

plt.figure()
plt.plot(f, x_)
plt.xlim(0, 5)

plt.figure()
plt.plot(f, y1)
plt.plot(f, y2)
plt.plot(f, y3)
plt.xlim(0, 5)
plt.ylim(0, 1)

#%%
def collectiveFreqResp():
    F = np.linspace(0, 6, 100)
    resp = np.zeros(100)
    Fs = 1000 # hz
    T = 10
    t = np.linspace(0, T, Fs*T)
    azim = 2*pi*t
    for i, f in enumerate(F):


        x = np.array([sin(f*2*pi*t), sin(f*2*pi*(t + 1/3)), sin(f*2*pi*(t + 2/3))]).T
        y = dq(x, azim, deg=False)

        freqs, x_ = freqResp(y[:,0], Fs)
        resp[i] = np.max(x_)
    return F, resp

F, resp = collectiveFreqResp()

