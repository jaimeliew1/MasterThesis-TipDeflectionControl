import numpy as np
import matplotlib.pyplot as plt
from Other.Weibull import wsp_probs

import math
def run(nothing, SAVE=False):


    P = wsp_probs()
    X, Y = zip(*P.items())
    x = np.linspace(0, 30, 1000)
    k = 2
    A = 10/math.gamma(1+1/k)
    y = k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)

    plt.figure(figsize=(5, 4))
    plt.bar(X, Y, width=2, alpha=0.5, label='Discrete')
    plt.plot(x, y, 'k', label='Continuous')
    plt.legend(title='Wind Speed Distributions')
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Probability [-]')
    plt.xlim(0, 27)
    plt.xticks(range(0, 27, 2))
    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')
    plt.show(); print()





if __name__ is '__main__':
    run(0, False)




