# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:08:20 2018

@author: J
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos

x = np.linspace(0, 2*pi, 100)


plt.plot(x, sin(x))
plt.plot(x, sin(3*x))
plt.plot(x, sin(3*x + 2*pi))