# -*- coding: utf-8 -*-
"""
Created on Wed Oct 6 10:12:02 2021

@author: sila
"""

from sklearn.datasets import load_digits
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

mnist = load_digits()

print("Data Shape:")
print(pd.DataFrame(mnist.data).shape)

print("Data Head:")
print(pd.DataFrame(mnist.data).head())

print("Target Shape:")
print(pd.DataFrame(mnist.target).shape)

fig, axes = plt.subplots(2, 10, figsize=(16, 6))
for i in range(20):
    axes[i // 10, i % 10].imshow(mnist.images[i], cmap='gray');
    axes[i // 10, i % 10].axis('off')
    axes[i // 10, i % 10].set_title(f"target: {mnist.target[i]}")

plt.tight_layout()

plt.show()

X_train, X_test, y_train, y_test = train_test_split(mnist.data,
                                                    mnist.target,
                                                   test_size=0.2,
                                                   random_state=0)

clf = RandomForestClassifier(n_estimators=3, max_depth=None)

clf.fit(X_train, y_train)
y_preds = clf.predict(X_test)

acc = accuracy_score(y_test, y_preds)

print(acc)

mat = confusion_matrix(y_test, y_preds)

print(mat)