
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from Modelling import BladeModel

def run( SAVE=False):
    models = BladeModel.make()
    # plot transfer function over frequency response
    WSP = [6, 12, 18, 24]
    models = [x for x in models if x.wsp in WSP]

    fig, axes = plt.subplots(2, 1, sharex=True)
    plt.subplots_adjust(hspace=0.05)
    axes[0].grid(axis='x', which='minor')
    axes[1].grid(axis='x', which='minor')
    axes[1].set_ylim([-180, 180])
    axes[0].set_xlim([0.05, 5])
    axes[0].set_xscale('log')
    axes[0].set_yscale('log')
    axes[0].set_ylim([1e-2, 1e2])
    axes[1].set_yticks(np.arange(-180, 121, 60))
    axes[0].set_ylabel('$|G(jw)|$ [dB]')
    axes[1].set_ylabel('$< G(jw)$ [deg]')
    axes[1].set_xlabel('Frequency [Hz]')
    F1p = 0.16
    axes[1].set_xticks([F1p, 2*F1p, 3*F1p, 4*F1p], minor=True)
    axes[1].set_xticklabels(['$f_{1p}$', '$f_{2p}$', '$f_{3p}$', '$f_{4p}$'], minor=True)

    for i, model in enumerate(models):
        w, h = signal.freqresp(model.tf)
        f = w/(2*np.pi)
        axes[0].plot(f, abs(h), lw=1, label=f'${WSP[i]}m/s$')
        axes[1].plot(f, np.angle(h, deg=True), '-', lw=1)

    axes[0].legend(title='Windspeed', loc='lower right', ncol=2)
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()




if __name__ == '__main__':
    run()

















