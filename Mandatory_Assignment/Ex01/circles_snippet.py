# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:23:02 2018

@author: sila
"""

from sklearn.datasets import make_circles;
import matplotlib.pyplot as plt

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

