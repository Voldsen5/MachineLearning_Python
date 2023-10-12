# -*- coding: utf-8 -*-
"""
Created on Mon December 9 10:41:37 2019

@author: sila
"""

from sklearn.model_selection import train_test_split
from sklearn import decomposition
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
import numpy as np

faces = datasets.fetch_olivetti_faces()
faces.data.shape

from matplotlib import pyplot as plt

fig = plt.figure(figsize=(8, 6))

# The faces are already scaled to the same size.
# Lets plot the first 20 of these faces.
for i in range(20):
    ax = fig.add_subplot(4, 5, i + 1, xticks=[], yticks=[])
    ax.imshow(faces.images[i], cmap=plt.cm.bone)
    ax.set_title(i, fontsize='small', color='green')

plt.show()

# As usual, then lest split the dataset in a train and a test dataset.
X_train, X_test, y_train, y_test = train_test_split(faces.data,
                                                    faces.target, random_state=0)

print(X_train.shape, X_test.shape)

# Lets downscale the orginal pics with PCA

# n_components = Number of components to keep,
# Whitening = true can soemtimes
# improve the predictive accuracy of the downstream estimators
# by making their data respect some hard-wired assumptions.

pca = decomposition.PCA(n_components=150, whiten=True)
pca.fit(X_train)

# lets look at some of these faces. The socalled eigenfaces.
fig = plt.figure(figsize=(16, 6))
for i in range(6):
    ax = fig.add_subplot(2, 3, i + 1, xticks=[], yticks=[])
    ax.imshow(pca.components_[i].reshape(faces.images[0].shape),
              cmap=plt.cm.bone)

plt.show()

# With a PCA projection, the original pictures, train and test,
# can now be projected onto the PCA basis:
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

print(X_train_pca.shape)
print(X_test_pca.shape)

# We now use a SVM to make a classification
# kernel default = rbf, gamma = kernel coefficient
clf = svm.SVC(kernel='linear',C=5., gamma=0.001)
clf.fit(X_train_pca, y_train)

# It is now time to evaluate how well this classification did.
# Lets look at the first 25 pics in he test set.
fig = plt.figure(figsize=(8, 6))
for i in range(25):
    ax = fig.add_subplot(5, 5, i + 1, xticks=[], yticks=[])
    ax.imshow(X_test[i].reshape(faces.images[0].shape),
              cmap=plt.cm.bone)
    y_pred = clf.predict(X_test_pca[i, np.newaxis])[0]
    color = ('blue' if y_pred == y_test[i] else 'red')
    ax.set_title(y_pred, fontsize='small', color=color)

y_pred = clf.predict(X_test_pca)
print(metrics.classification_report(y_test, y_pred))
plt.show()





