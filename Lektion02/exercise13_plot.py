# -*- coding: utf-8 -*-

# Python version
import matplotlib.pyplot as plt
import numpy as np


def cost(a,b,X,y):
     ### Evaluate half MSE (Mean square error)
     m = len(y)
     error = a + b*X - y
     J = np.sum(error ** 2)/(2*m)
     return J

X = 2 * np.random.rand(5, 1)
y = 4 + 3 * X + np.random.randn(5, 1)

ainterval = np.arange(3,5, 0.05)
binterval = np.arange(2,4, 0.05)

low = cost(0,0, X, y)
bestatheta = 0
bestbtheta = 0
for atheta in ainterval:
    for btheta in binterval:
        print("xy: %f:%f:%f" % (atheta,btheta,cost(atheta,btheta, X, y)))
        if (cost(atheta,btheta, X, y) < low):
           low = cost(atheta,btheta, X, y)
           bestatheta = atheta
           bestbtheta = btheta

plt.plot(X,y, "b.")
plt.axis([0,2,0,15])


plt.plot()
plt.show()