import numpy as np
import math

def pdf(wsp, A, k):
    # returns the probability density at wind speed wsp for a weibull
    # distribution described by the parameters A and k.
    pdf = lambda x: k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)

    return pdf(wsp)

def cdf(wsp, A, k):
    # returns the cumulative density at wind speed wsp for a weibull
    # distribution described by the parameters A and k.
    cdf = lambda x: 1 - np.exp(-(x/A)**k)

    return cdf(wsp)

def wsp_probs(Class=1, dx=2, Range= [4, 26.1]):
    # Weibull Parameters
    k = 2
    if Class == 1:
        A = 10/math.gamma(1+1/k)
    elif Class == 2:
        A = 8.5/math.gamma(1+1/k)
    elif Class == 3:
        A = 7.5/math.gamma(1+1/k)
    #print(A)
    # Weibull cdf function
    cdf = lambda x: 1 - np.exp(-(x/A)**k)
    #Discrete wind speeds
    Y = np.arange(Range[0], Range[1], dx)

    # Probabilities of each wind speed
    P = [(cdf(y+dx/2) - cdf(y-dx/2)) for y in Y]

    return dict(zip(Y, P))


if __name__ == '__main__':
    p = wsp_probs()