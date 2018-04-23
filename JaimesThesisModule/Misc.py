#Jaime Liew
#s141777

#Version 1.00
#feb 26 2018

#a collection of functions I am using for my master thesis

import numpy as np
import pandas as pd
from collections import deque, defaultdict
import matplotlib.pyplot as plt
from scipy import signal
pi = np.pi

def readHawc2Res(filename,channels=None):
    #reads specific channels of HAWC2 binary output files and saves in a
    #pandas dataframe. Variable names and channels are defined in a dictionary
    # called channels

    if channels is None:

        channels = {
            't'         : 1,    #time [s]
            'wsp'       : 15,   #wind speed [m/s]
            'Paero'     : 12,   #aerodynamic power [?]
            'Pelec'     :100,   #electrical power [W]
            'Azim'      :  2,   #rotor azimuth angle [deg]
            'RBM1'      : 26,   #root bending moment - blade 1 [kNm]
            'RBM2'      : 29,
            'RBM3'      : 32,
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


    #read .sel file
    with open(filename + '.sel') as f:
        lines = f.readlines()

    NCh             = int(lines[8].split()[1])
    NSc             = int(lines[8].split()[0])
    Format          = lines[8].split()[3]
    scaleFactor     = [float(x) for x in lines[NCh+14:]]

    #read .bin file
    data = {}
    fid = open(filename + '.dat', 'rb')
    for key,ch in channels.items():
        fid.seek((ch-1)*NSc*2)
        data[key] = np.fromfile(fid,'int16',NSc) * scaleFactor[ch-1]


    return pd.DataFrame(data)


def FilterToHTC(B,A,filename):
    assert len(B) == len(A)
    N = len(B)
    with open(filename,'w') as f:
        f.write('\t\tconstant 1       {:<25} ; N  Length of filter\n'.format(N))
        #f.write('\t\tconstant 2       {:<25} ; Kp Gain of controller [rad/m]\n'.format(k))

        f.write('\t\t; Feed-Forward Coefficients\n')
        for i in range(N):
            f.write('\t\tconstant {:<4}    {:<25} ; b{}\n'.format(3+i,B[i],i))

        f.write('\t\t; Feed-Backward Coefficients\n')
        for i in range(N):
            f.write('\t\tconstant {:<4}    {:<25} ; a{}\n'.format(N+3+i,A[i],i))



def bodePlot(title='',F1p=None):
    #sets up figure for a bode plot. passes back axes = (ax1, ax2)
    fig, axes = plt.subplots(2,1,figsize=[7,6],sharex=True)
    plt.subplots_adjust(hspace=0.05)
    axes[0].set_title(title)
    axes[0].set_ylabel('Magnitude [dB]')
    axes[1].set_ylabel('Phase [deg]')
    axes[1].set_xlabel('Frequency [Hz]')

    axes[1].set_ylim([-180,180])
    axes[0].set_xlim([0,1.5])
    axes[0].set_ylim([-50,20])
    axes[1].set_yticks(np.arange(-180,181,60))
    if F1p is not None:
        for i in range(4):
            axes[0].axvline(x=F1p*(i+1),linestyle='--',color='k',lw=1)
            axes[1].axvline(x=F1p*(i+1),linestyle='--',color='k',lw=1)
    axes[0].axhline(y=1,linestyle='--',color='0.7',lw=1)
    return fig, axes

def plotFreq(axes,b,a,Fs=None,label='',ls='-',RES=2048*8):
    #plots frequency response of digital filter defined by coefficients, b and a.
    #plots on axes = (ax1,ax2)
    if Fs is None: #continuous
        w,h = signal.freqs(b,a,worN=RES)
        f       = w/(2*pi)
    else:
        w,h = signal.freqz(b,a,worN=RES)
        f       = w*(Fs/2)/pi
    mag     = 20 * np.log10(abs(h))
    phase   = np.angle(h,deg=True)
    axes[0].plot(f,mag,ls,label=label)
    axes[1].plot(f,phase,ls)
    axes[0].legend()





class SingleBladeController(object):
    def __init__(self,array1):

        self.N = array1[0] # order of filter
        self.K = array1[1] # Proportional gain of filter
        self.b = array1[2:(2 + self.N)] #Numerator coefficients of filter
        self.a = array1[(2 + self.N):(2 + 2*self.N)] #Denominator coefficients of filter
        #note. len(b) == len(a) == N

        #placeholders for storing the past N inputs and outputs. Assumes 3 blades
        self.x_ = np.zeros([3,self.N])
        self.y_ = np.zeros([3,self.N])

    def update(self,array1):
        t           = array1[0]   #Simulation time
        theta       = array1[1:4] #Power pitch demand
        x           = array1[4:7] #Root moment or tip deflection
        # Center about the mean
        x           = x - np.mean(x)

        # shift index of past states by 1. eg: [1,2,3,4] -> [4,1,2,3]
        N = self.N
        self.x_[:,1:N] = self.x_[:,0:N-1]
        self.y_[:,1:N] = self.y_[:,0:N-1]
        self.x_[:,0]     = x
        self.y_[:,0]     = [0,0,0]

        #apply filter to x_ and y_ to find newest y_
        for i in [0,1,2]:       # For each blade...
            for j in range(N):  # for each past input and output value...
                                # apply filter coefficients.
                self.y_[i,0] += self.b[j]* self.x_[i,j] - self.a[j]*self.y_[i,j]

        #Calculate control feedback action
        theta_ = -self.K*self.y_[:,0]

        #Superimpose IPC control action (theta_) over power pitch demand (theta)
        out = list(theta + theta_)

        return out



def generateHTC(filename_main, filename_template, htc_params):
    with open(filename_template) as f:
        htcText = f.read()
    for key, value in htc_params.items():
        htcText = htcText.replace(key,str(value))
    with open(filename_main,'w') as f:
        f.write(htcText)

def getTemplateParams(filename_template):
    with open(filename_template) as f:
        data = f.read()
    params = [x.split('}')[0] for x in a.split('{')[1:]]
    return list(set(params))


"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
__version__ = "1.0.1"

#from collections import deque, defaultdict
#import numpy as np

def reversals(series):
    """
    A generator function which iterates over the reversals in the iterable
    *series*. Reversals are the points at which the first
    derivative on the series changes sign. The generator never yields
    the first and the last points in the series.
    """
    series = iter(series)

    x_last, x = next(series), next(series)
    d_last = (x - x_last)

    for x_next in series:
        if x_next == x:
            continue
        d_next = x_next - x
        if d_last * d_next < 0:
            yield x
        x_last, x = x, x_next
        d_last = d_next



def extract_cycles(series):
    """
    Returns two lists: the first one containig full cycles and the second
    containing one-half cycles. The cycles are extracted from the iterable
    *series* according to section 5.4.4 in ASTM E1049 (2011).
    """
    points = deque()
    full, half = [], []

    for x in reversals(series):
        points.append(x)
        while len(points) >= 3:
            # Form ranges X and Y from the three most recent points
            X = abs(points[-2] - points[-1])
            Y = abs(points[-3] - points[-2])

            if X < Y:
                # Read the next point
                break
            elif len(points) == 3:
                # Y contains the starting point
                # Count Y as one-half cycle and discard the first point
                half.append(Y)
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                full.append(Y)
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            half.append(abs(points[-2] - points[-1]))
            points.pop()
    return full, half



def rainflow(series, ndigits=None):
    """
    Returns a sorted list containig pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers. The cycles are extracted from the iterable *series*
    using the extract_cycles function. If *ndigits* is given the cycles
    will be rounded to the given number of digits before counting.
    """
    full, half = extract_cycles(series)

    # Round the cycles if requested
    if ndigits is not None:
        full = (round(x, ndigits) for x in full)
        half = (round(x, ndigits) for x in half)

    # Count cycles
    counts = defaultdict(float)
    for x in full:
        counts[x] += 1.0
    for x in half:
        counts[x] += 0.5

    output = np.array(sorted(counts.items()))
    return output[:,0], output[:,1] #stress, count



def EquivalentLoad(data, neq, m):
    #!!! use rainflow module
    S, C = rainflow(data) #Stress level, number of cycles
    nrSum = 0
    for s, c in zip(S,C):
        nrSum += c*s**m
    Req =(nrSum/neq)**(1/m)

    stressBins = np.linspace(0,max(S),20)[1:] # Max value of each bin
    stressCycles = np.zeros(len(stressBins))

    for i in range(len(stressBins)-1):
        stressCycles[i] = sum(C[(stressBins[i] < S) & (stressBins[i+1] > S)])
    return Req, stressBins, stressCycles





