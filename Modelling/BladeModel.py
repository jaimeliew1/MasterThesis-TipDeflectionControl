import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy import signal

#rc('text', usetex=True)
class BladeModel(object):
    pass

def plotModels(models, save=False):
    # plot transfer function over frequency response
    for model in models:
        w, h = signal.freqresp(model.tf)

        fig, axes = plt.subplots(2, 1, sharex=True)
        plt.subplots_adjust(hspace=0.05)
        axes[0].grid('off')
        axes[1].grid('off')
        fig.suptitle('wsp: {}'.format(model.wsp))
        axes[0].set_ylabel('|G(jw)| [dB]')
        axes[1].set_ylabel('$\ angle$ G(jw) [deg]')
        axes[1].set_xlabel('Frequency [rad/s]')

        axes[1].set_ylim([-180, 180])
        axes[0].set_xlim([0.1, 30])
        axes[0].set_xscale('log')
        axes[0].set_yscale('log')
        #axes[0].set_ylim([1e-2, 1e2])
        axes[1].set_yticks(np.arange(-180, 121, 60))



        axes[0].plot(model.f, abs(model.G), lw=1, label='Spectral')
        axes[0].plot(w,abs(h), '--', lw=1, label='Approximation')

        axes[1].plot(model.f, np.angle(model.G, deg=True), lw=1)
        axes[1].plot(w, np.angle(h, deg=True), '--', lw=1)
        if save:
            plt.savefig('../Figures/Blade_TF_{}.png'.format(model.wsp), dpi=200)

        plt.show(); print()




def make():
    resDir = 'Data/'
    resDir = '../Modelling/Data/'
    models = []

    # load frequency response data of blade system
    filenames = [x for x in os.listdir(resDir) if 'FreqRespFunc_' in x]

    for file in filenames:
        mat = sio.loadmat(resDir + file)
        models.append(BladeModel())
        models[-1].f = np.reshape(mat['om'], [-1])
        models[-1].G = np.reshape(mat['g'], [-1])
        models[-1].wsp = int(file.split('_')[1][:-4])

    # load transfer function approximation for blade systems
    filenames = [x for x in os.listdir(resDir) if 'TransferFunc_' in x]

    for i, file in enumerate(filenames):
        mat = sio.loadmat(resDir + file)
        models[i].b = np.reshape(mat['b'],[-1])
        models[i].a = np.reshape(mat['a'],[-1])
        models[i].tf = signal.TransferFunction(models[i].b, models[i].a)

    # sort models by wind speed
    sortIndices = np.argsort([x.wsp for x in models])
    models = [models[i] for i in sortIndices]

    return models

def modelTransferFunctions():
    models = make()
    return [x.tf for x in models]

def Blade(wsp):
    # returns the blade model transfer function for windspeed wsp
    assert wsp%2 == 0
    models = make()
    return models[(wsp-4)//2].tf




if __name__ == '__main__':
    models = make()
    plotModels(models, save=False)


















