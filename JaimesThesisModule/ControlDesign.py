# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:46:41 2018

@author: J
"""

import matplotlib.pyplot as plt
from scipy import signal
from numpy import poly1d
import numpy as np


class Turbine(object):
    # a wrapper object for the transfer functions describing a wind turbine
    # with tip deflection control.Used to evaluate a controller

    def __init__(self, P, C):
        # Initiated with a plant transfer function, P, and a controller
        # transfer function, C. Both are scipy.signal.TransferFunction
        # objects.
        self.P = P
        self.C = C

    @property
    def sm(self):
        # Returns the stability margin of the system
        w_ = np.linspace(0, 1.5, 10000)*2*np.pi
        w_ = np.append(w_, [100])

        w, H = signal.freqresp(self.L, w=w_)

        return min(np.sqrt((H.real + 1)**2 + H.imag**2))

    @property
    def L(self):
    # Returns the loop transfer function, L = PK given a plant and controller
    # transfer function (scipy.signal.TransferFunction objects)
        num = np.polymul(self.P.num, self.C.num)
        den = np.polymul(self.P.den, self.C.den)

        return signal.TransferFunction(num, den)
    @property
    def S(self):
        # returns the sensitivity function, S = 1/(1+L) given a plant and
        # controller transfer function (scipy.signal.TransferFunction objects)
        L_ = self.L

        den = (poly1d(L_.den) + poly1d(L_.num)).c
        num = L_.den

        return signal.TransferFunction(num, den)
    @property
    def CL(self):
        # returns the close loop transfer function, G_cl = PS given a plant and
        # controller transfer function (scipy.signal.TransferFunction objects)
        S_ = self.S

        den = np.polymul(self.P.den, S_.den)
        num = np.polymul(self.P.num, S_.num)

        return signal.TransferFunction(num, den)



 #TODO Update this so that it can be easily inherited.
class Controller2(object):
    # A class for designing an IPC controller with transfer function, C. Uses
    # a provided blade transfer function, P which describes pitch to tip
    # deflection system.

    def __init__(self, Ts=None):
        self.Ts = Ts
        self.K = 1

        self.poles = []
        self.zeros = []

    def __call__(self, f):
        # Returns coefficients of the protofilter scaled so that F1P is at
        # a new frequency, f. This is achieved changing the sampling time
        # of the filter.
        Ts_des = f/self.F1P * self.Ts
        b_, a_ = self.bilinear(Ts_des)

        return b_, a_

    def addPolePair(self, omega, zeta):
        if np.isscalar(omega):
            omega, zeta = [omega], [zeta]

        for o, z in zip(omega, zeta):
            Re = -z*o
            Im = o*np.sqrt(1 - z**2)
            self.poles.append(Re + 1j*Im)
            self.poles.append(Re - 1j*Im)

    def addZeroPair(self, omega, zeta):
        if np.isscalar(omega):
            omega, zeta = [omega], [zeta]

        for o, z in zip(omega, zeta):
            Re = -z*o
            Im = o*np.sqrt(1 - z**2)
            self.zeros.append(Re + 1j*Im)
            self.zeros.append(Re - 1j*Im)

    def addPole(self, P):
        if np.isscalar(P):
            P = [P]
        for p in P:
            self.poles.append(p)

    def addZero(self, Z):
        if np.isscalar(Z):
            Z = [Z]
        for z in Z:
            self.zeros.append(z)

    def addLeadCompensator(self, lead, freq):
    # Adds the pole and zero for lead compensation which adds 'lead'
    # amount of phase [deg] at 'freq' [Hz]
        lead = lead * np.pi/180
        freq = freq * 2 *np.pi

        a = (1 + np.sin(lead))/(1 - np.sin(lead))
        T = 1/(np.sqrt(a) * freq)
        self.addPole(-1/T)
        self.addZero(-1/(a*T))

    def freqResp(self, om, hz=True):
        # returns the magnitude [dB] and phase [deg] response at frequency f.
        if hz:
            om = om*2*np.pi
        w, h = self.freqs()
        mag = np.interp(om, w, abs(h))
        ang = np.interp(om, w, np.angle(h, deg=True))
        return mag, ang

    def freqs(self):
        return signal.freqs(self.b, self.a)

    def bilinear(self, Ts=None):
        if Ts is None:
            Ts = self.Ts
        return signal.bilinear(self.b, self.a, 1/Ts)

    @property
    def a(self):
        return np.array(poly1d(self.poles, r=True))

    @property
    def b(self):
        return np.array(self.K*poly1d(self.zeros, r=True))

    @property
    def coefs(self):
        return self.b, self.a

    @property
    def coefz(self):
        return self.bilinear()

    @property
    def tf(self):
        # Returns continuous transfer function
        return signal.ZerosPolesGain(self.zeros, self.poles, self.K).to_tf()

    @property
    def tfz(self):
        # Returns discrete transfer function
        return signal.TransferFunction(*self.coefz, dt=self.Ts)





def _stabilityMargin( w, H):
    ind_min = np.argmin(np.sqrt((H.real + 1)**2 + H.imag**2))
    #sm_w = w[ind_min]
    #sm = np.sqrt((H[ind_min].real + 1)**2 + H[ind_min].imag**2)

    return H[ind_min]


class Controller(object):

    def __init__(self, name='', Ts=None):
        self._name = name
        self.Ts = Ts
        self.K = 1
        self.poles = []
        self.zeros = []
        self.b = []
        self.a = []

    def addPolePair(self, omega, zeta):
        if np.isscalar(omega):
            omega, zeta = [omega], [zeta]

        for o, z in zip(omega, zeta):
            Re = -z*o
            Im = o*np.sqrt(1 - z**2)
            self.poles.append(Re + 1j*Im)
            self.poles.append(Re - 1j*Im)

        self.b = poly1d(self.zeros, r=True)
        self.a = poly1d(self.poles, r=True)

    def addZeroPair(self, omega, zeta):
        if np.isscalar(omega):
            omega, zeta = [omega], [zeta]

        for o, z in zip(omega, zeta):
            Re = -z*o
            Im = o*np.sqrt(1 - z**2)
            self.zeros.append(Re + 1j*Im)
            self.zeros.append(Re - 1j*Im)

        self.b = poly1d(self.zeros, r=True)
        self.a = poly1d(self.poles, r=True)

        self.b = poly1d(self.zeros, r=True)
        self.a = poly1d(self.poles, r=True)

    def addPole(self, P):
        if np.isscalar(P):
            P = [P]
        for p in P:
            self.poles.append(p)

        self.b = poly1d(self.zeros, r=True)
        self.a = poly1d(self.poles, r=True)

    def addZero(self, Z):
        if np.isscalar(Z):
            Z = [Z]
        for z in Z:
            self.zeros.append(z)

        self.b = poly1d(self.zeros, r=True)
        self.a = poly1d(self.poles, r=True)

    def freqResp(self, om):
        # returns the magnitude [dB] and phase [deg] response at frequency f.
        w, h = self.freqs()
        resp = np.interp(om, w, h)
        return abs(h), np.angle(h, deg=True)

    def freqs(self):
        return signal.freqs(self.b, self.a)

    def coefs(self, disc=None):
        if disc == None:
            #return continuous coefficients
            return self.b*self.K, self.a

        elif disc.lower() == 'matched':
            # return discrete coefficients using matched zero pole method
            return MatchedZeroPole(self.b*self.K, self.a, self.Ts)

        elif disc.lower() == 'bilinear':
            # return discrete coefficients using bilinear method
            return signal.bilinear(self.b*self.K, self.a, 1/self.Ts)

    def saveHTC(self, filename, disc='bilinear'):
        if disc.lower() == 'matched':
            # return discrete coefficients using matched zero pole method
            b, a = MatchedZeroPole(self.b*self.K, self.a, self.Ts)

        elif disc.lower() == 'bilinear':
            # return discrete coefficients using bilinear method
            b, a = signal.bilinear(self.b*self.K, self.a, 1/self.Ts)
        saveHTC(b, a, filename)


def saveHTC(B, A, filename):
    M = len(A)
    b_ = np.pad(B, [0, M], 'constant')[:M]
    a_ = np.pad(A, [0, M], 'constant')[:M]
    N = len(a_)
    with open(filename, 'w') as f:
        f.write('\t\tconstant 1       {:<25} ; N  Length of filter\n'.format(N))
        #f.write('\t\tconstant 2       {:<25} ; Kp Gain of controller [rad/m]\n'.format(k))

        f.write('\t\t; Feed-Forward Coefficients\n')
        for i in range(N):
            f.write('\t\tconstant {:<4}    {:<25} ; b{}\n'.format(3+i,b_[i],i))

        f.write('\t\t; Feed-Backward Coefficients\n')
        for i in range(N):
            f.write('\t\tconstant {:<4}    {:<25} ; a{}\n'.format(N+3+i,a_[i],i))



def MatchedZeroPole(b, a, TS):
    #converTS continuous transfer function b,a to discrete transfer function, bd, ad.
    #Uses pole/zero/DC gain matching.
    b, a = poly1d(b), poly1d(a)
    DC_c = b.coeffs[-1]/a.coeffs[-1]
    #Find discrete zeros and poles
    zeros_d = np.exp(b.roots*TS)
    poles_d = np.exp(a.roots*TS)
    #adds discrete zeros at z=-1 to account for continuous zeros at infinity
    NzerosAtInf = len(poles_d) - len(zeros_d)
    zeros_d = np.append(zeros_d, -np.ones(NzerosAtInf))
    #Calculate discrete transfer function from discrete poles and zeros
    bd = poly1d(zeros_d, r=True)
    ad = poly1d(poles_d, r=True)
    #match DC gains
    DC_d = sum(bd.coeffs)/sum(ad.coeffs)
    bd = bd/DC_d*DC_c
    return bd.c, ad.c

def bode(*args, title='', F1p=None, xlim=[0, 1.5], logscale=True):
    #sets up figure for a bode plot. passes back axes = (ax1, ax2)
    fig, axes = plt.subplots(2, 1, figsize=[6,6], sharex=True)
    plt.subplots_adjust(hspace=0.05)
    axes[0].grid('off')
    axes[1].grid('off')
    axes[0].set_title(title)
    axes[0].set_ylabel('Magnitude [dB]')
    axes[1].set_ylabel('Phase [deg]')
    axes[1].set_xlabel('Frequency [Hz]')

    #axes[1].set_ylim([-180, 180])
    axes[0].set_xlim(xlim)
    #axes[0].set_ylim([-50, 20])
    axes[1].set_yticks(np.arange(-180, 181, 60))

    if logscale:
        axes[0].set_xlim([0.01, xlim[1]])
        #axes[0].set_ylim([0.000001, 1e3])
        axes[0].set_xscale('log')
        #axes[0].set_yscale('log')
    if F1p is not None:
        for i in range(4):
            #axes[0].text(F1p*(i+1)+0.005, 10, '{}P'.format(i+1))
            axes[0].axvline(x=F1p*(i+1), linestyle='--',color='k', lw=1)
            axes[1].axvline(x=F1p*(i+1), linestyle='--',color='k', lw=1)
    axes[0].axhline(y=0, linestyle='--', color='0.7', lw=1)

    for tf in args:
        w_ = np.linspace(*xlim, 1000)*2*np.pi
        w, mag, phase = signal.bode(tf, w=w_)
        axes[0].plot(w/(2*np.pi), mag)
        axes[1].plot(w/(2*np.pi), phase)
    return fig, axes

def nyquist(*args, ax=None, title='', zoom=None, save=False, N=1e4):

    # Make axis if not given
    if not ax:
        fig, ax = plt.subplots()

    t_ = np.linspace(0, 2*np.pi, 100)
    circx, circy = np.sin(t_), np.cos(t_)
    ax.axis('equal')
    ax.plot(circx, circy, '--', lw=1, c='0.7')
    ax.plot([-1], [0], 'xr')

    #ax.plot([-1, L(f_sm).real], [0, L(f_sm).imag], '--r', lw=0.5)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    if zoom:
        ax.set_xlim(zoom)
        ax.set_ylim(zoom)

    w_ = np.linspace(0, 1.5, N)*2*np.pi
    w_ = np.append(w_, [100])
    for tf in args:
        w, H = signal.freqresp(tf, w=w_)
        ax.plot(H.real, H.imag, 'k', lw=1)
        ax.plot(H.real, -H.imag, '--k', lw=1)


        H_ = _stabilityMargin(w, H)
        ax.plot([-1, H_.real], [0, H_.imag], '--r', lw=0.5)

    if save:
        plt.savefig(save, dpi=200)

    return fig, ax
def plotFreq(axes, b, a, Fs=None, label='', ls='-', RES=2048*8):
    #plots frequency response of digital filter defined by coefficients, b and a.
    #plots on axes = (ax1,ax2)
    if Fs is None: #continuous
        w, h = signal.freqs(b, a, worN=RES)
        f       = w/(2*np.pi)
    else:
        w, h = signal.freqz(b, a, worN=RES)
        f       = w*(Fs/2)/np.pi
    mag     = 20 * np.log10(abs(h))
    phase   = np.angle(h, deg=True)
    axes[0].plot(f, mag, ls, label=label)
    axes[1].plot(f, phase, ls)
    axes[0].legend()





