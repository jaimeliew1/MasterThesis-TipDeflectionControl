
from JaimesThesisModule.Misc import readHawc2Res
import numpy as np
from numpy.fft import fft
from scipy import signal
import matplotlib.pyplot as plt



def loadData(fn='C:/JL0004/res/dlc11_0/dlc11_0_noipc_000_04_1004'):
    data = readHawc2Res(fn)
    t, x = data.t, data.TD1
    return t, x


###### FFT methods ###########
def freqResp(x, Fs):
    N = len(x)
    f  = np.linspace(0, Fs, N)
    Y = 2/N*abs(fft(x))

    return f, Y

def PSD(x, Fs):
    N = len(x)
    x -= np.mean(x)
    f  = np.linspace(0, Fs, N)
    Y = 2/(N*Fs)*abs(fft(x))**2

    return f[f<=Fs/2], Y[f<=Fs/2]

# THIS ONE WORKS
def meanPSD(X, Fs, nperseg=5000):
    N = len(X)//nperseg*nperseg

    Y = np.zeros(nperseg)
    X -= np.mean(X)
    f  = np.linspace(0, Fs, nperseg)
    X = np.reshape(X[:N*nperseg], [-1, nperseg])
    for x in X:
        Y += 2/(N*Fs)*abs(fft(x))**2

    return f[f<=Fs/2], Y[f<=Fs/2]



def meanfreqResp(X, Fs, nperseg=20000):
    N = len(X)//nperseg*nperseg
    K = N//nperseg
    f  = np.linspace(0, Fs, nperseg)
    Y = np.zeros(nperseg)

    X = np.reshape(X[:N*nperseg], [-1, nperseg])
    for x in X:
        Y += 2/(nperseg*K)*abs(fft(x))

    return f, Y



def PSDtest(t, x, Fs, methods):

    variance = np.var(x)
    N = len(methods)

    # Calculate PSD using different methods
    F, Y = [], []
    for method in methods:
        F.append([])
        Y.append([])
        F[-1], Y[-1] = method(x, Fs)


    # Compare variance with area under curve
    area = np.zeros(N)
    print(f'Actual area: {variance:2.6f}')
    for i in range(N):
        area[i] = np.trapz(Y[i], x=F[i])
        print(f'{area[i]:2.6f}')

    plt.figure()
    plt.ylim(1e-4, 100)
    plt.xlim(0.1, 10)
    plt.xscale('log')
    plt.yscale('log')
    for f, y in zip(F, Y):
        plt.plot(f, y)



def fftTest(t, x, Fs, methods):
# Calculate PSD using different methods
    F, Y = [], []
    for method in methods:
        F.append([])
        Y.append([])
        F[-1], Y[-1] = method(x, Fs)


    plt.figure()
    #plt.ylim(1e-4, 10)
    plt.xlim(0.1, 2)
    #plt.xscale('log')
    #plt.yscale('log')
    for i, (f, y) in enumerate(zip(F, Y)):
        plt.plot(f, np.sqrt((Fs/len(y))*y), label=f'{i}')
    plt.legend()
    plt.grid()




methods = [PSD, signal.periodogram, meanPSD]
#methods = [meanPSD]
t, x = loadData()
#x = 8*np.sin(t*3) + 3*np.sin(8*t)
#####################
PSDtest(t, x, 100, methods)

fftTest(t, x, 100, methods)




