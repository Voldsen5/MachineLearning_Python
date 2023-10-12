# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 20:23:27 2018

@author: Sila
"""

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

X = 2 * np.random.rand(500, 1)
y = 4 + 3 * X + np.random.randn(500, 1)

lm = linear_model.LinearRegression()
model = lm.fit(X,y)


plt.plot(X,y, "g.")
plt.axis([0,2,0,15])

#fit function
f = lambda x: lm.coef_*x + lm.intercept_

plt.plot(X,f(X), c="red")

plt.plot()
plt.show()

