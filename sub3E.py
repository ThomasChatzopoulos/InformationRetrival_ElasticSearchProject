import json  
import hdbscan

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN

def clustering_results(resultMatrix,algorithmName):
    print('---',algorithmName,'---')
    labels_unique = np.unique(resultMatrix)
    minValue = min(resultMatrix)
    n_clusters = len(labels_unique)
    print('Number of clusters:',n_clusters)
    clusters = [0] * (n_clusters)
    print('min:',min(resultMatrix))
    for value in resultMatrix:
        clusters[value-minValue] += 1
    print('Clusters population:',clusters)

with open('tempdata.json',encoding='utf8') as f:
    users = json.load(f)

genres = []
for genre in users[0]:
    if(not genre in genres and genre != 'userId'):
        genres.append(genre)

usersMatrix = []
for item in users:
    tempVector = []
    for genre in genres:
        tempVector.append(item[genre])
    usersMatrix.append(tempVector)
#HDBSCAN------------------------------------
clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,
    gen_min_span_tree=False, leaf_size=40,
    metric='euclidean', min_cluster_size=2, min_samples=None, p=None)
clusterer.fit(usersMatrix)

clustering_results(clusterer.labels_,'HDBSCAN')
print(clusterer.labels_)
#Mean Shift---------------------------------
bandwidth = estimate_bandwidth(usersMatrix, quantile=0.2)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(usersMatrix)

clustering_results(ms.labels_,'MeanShift')
#DBSCAN-------------------------------------
db = DBSCAN(eps=0.9, min_samples=5).fit(usersMatrix)
# print(db.labels_)
clustering_results(db.labels_,'DBSCAN')
