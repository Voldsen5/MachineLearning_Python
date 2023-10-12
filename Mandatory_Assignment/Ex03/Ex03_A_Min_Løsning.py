from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

iris_df = datasets.load_

pca = PCA(2)
X, y = iris_df.data, iris_df.target
X_proj = pca.fit_transform(X)
print(X_proj.shape)


colormap = np.array(['red', 'lime','yellow','grey','black','pink','purple','blue','brown','gold'])

for i in range(1,11):
    k = i
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X_proj)

    labels = kmeans.labels_

    plt.scatter(X_proj[:, 0], X_proj[:, 1], c=colormap[labels], s=40)
    plt.title('K Mean Classification')
    plt.show();

k = 3
kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X_proj)

labels = kmeans.labels_

plt.scatter(X_proj[:, 0], X_proj[:, 1], c=colormap[labels], s=40)
plt.title('K Mean Classification')
plt.show();