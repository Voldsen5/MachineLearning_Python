# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 14:29:21 2021

@author: sila
"""

import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

n_samples = 200
blob_centers = ([1, 1], [3, 4], [1, 3.3], [3.5, 1.8])
data, labels = make_blobs(n_samples=n_samples,
                          centers=blob_centers,
                          cluster_std=0.5,
                          random_state=0)

colours = ('green', 'orange', "blue", "magenta")
fig, ax = plt.subplots()

for n_class in range(len(blob_centers)):
    ax.scatter(data[labels == n_class][:, 0],
               data[labels == n_class][:, 1],
               c=colours[n_class],
               s=30,
               label=str(n_class))

plt.show()

# Split in train and test set
from sklearn.model_selection import train_test_split

datasets = train_test_split(data,
                            labels,
                            test_size=0.2)

X_train, X_test, y_train, y_test = datasets

# Feature scaling
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(10), max_iter=100)
mlp.fit(X_train, y_train)

# predictions
predictions = mlp.predict(X_test)

print(predictions)

import numpy as np

h = .02  # step size in the mesh

# create a mesh to plot in
x_min, x_max = X_test[:, 0].min() - 1, X_test[:, 0].max() + 1
y_min, y_max = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

plt.subplot(1, 1, 1)
plt.subplots_adjust(wspace=0.4, hspace=0.4)

Z = mlp.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# Plot also the training points
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
plt.xlabel('Y length')
plt.ylabel('X width')
plt.title("MLP")

plt.show()
