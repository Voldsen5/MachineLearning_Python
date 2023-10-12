# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 20:23:27 2018

@author: Sila
"""

import matplotlib.pyplot as plt
import numpy as np

X = 2 * np.random.rand(50, 1)
y = 4 + 3 * X + np.random.randn(50, 1)
print(X)
X_b = np.c_[np.ones((50, 1)), X]
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

X_new = np.array([[0],[2]])
X_new_b = np.c_[np.ones((2,1)), X_new]
y_predict = X_new_b.dot(theta_best)


plt.plot(X,y, "g.")
plt.axis([0,2,0,15])
plt.plot(X_new, y_predict, "r-")

plt.plot()
plt.show()

