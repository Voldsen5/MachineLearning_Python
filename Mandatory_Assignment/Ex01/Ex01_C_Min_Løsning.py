# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:23:02 2018

@author: sila
"""

from sklearn.datasets import make_circles;
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

from matplotlib import pyplot
from pandas import DataFrame
# generate 2d classification dataset
# generate 2d classification dataset
X, y = make_circles(n_samples=100, noise=0.05)
# scatter plot, dots colored by class value
df = DataFrame(dict(x=X[:,0], y=X[:,1], label=y))
colors = {0:'red', 1:'blue'}
fig, ax = pyplot.subplots()
grouped = df.groupby('label')
for key, group in grouped:
    group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key])
pyplot.show()



x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

h=0.01

xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

plt.subplot(1, 1, 1)
plt.subplots_adjust(wspace=0.4, hspace=0.4)

rbf_svc = svm.SVC(kernel='rbf', gamma=1.0).fit(X,y)
Z = rbf_svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
plt.text(0, -1.2, 'SVM rbf', fontsize=12, color='red')

pyplot.show()

poly_svc = svm.SVC(kernel='poly', gamma=1.0).fit(X,y)
Z = poly_svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
plt.text(0, -1.2, 'SVM poly', fontsize=12, color='red')

pyplot.show()

linear_svc = svm.SVC(kernel='linear', gamma=1.0).fit(X,y)
Z = linear_svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
plt.text(0, -1.2, 'SVM linear', fontsize=12, color='red')

pyplot.show()