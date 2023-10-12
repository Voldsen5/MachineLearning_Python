# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:54:51 2018

@author: Sila
"""

import matplotlib.pyplot as plt
import numpy as np
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
plt.plot(X,y, "b.")
plt.axis([0,2,0,15])
plt.plot()
plt.show()

print(X)
print(y)


X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

plt.plot(X, y, "b.")
plt.axis([0, 2, 0, 15])
plt.xlabel('X')
plt.ylabel('y')
plt.title('Random Data Points')
plt.show()

print(X)
print(y)
