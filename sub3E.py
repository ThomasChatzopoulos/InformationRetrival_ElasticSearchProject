import json  
import hdbscan
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN, OPTICS, cluster_optics_dbscan

from collections import Counter

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
print(genres)
# rawMatrix = []
usersMatrix = []
for item in users:
    tempVector = []
    for genre in genres:
        # rawMatrix.append(item[genre])
        tempVector.append(item[genre])
    usersMatrix.append(tempVector)

# for x in range(len(rawMatrix)):
#     rawMatrix[x] = round(rawMatrix[x] *10)/10
#     # print(rawMatrix[x])
# print(Counter(rawMatrix))

# print('Maximum:',max(rawMatrix))
# print('Minimum:',min(rawMatrix))
maximum = max(map(max,usersMatrix))
minimum = min(map(min,usersMatrix))
print('Maximum:',maximum)
print('Minimum:',minimum)

usersMatrix = [[round(value-minimum,4) for value in vector] for vector in usersMatrix]
# print(usersMatrix)

#HDBSCAN------------------------------------
clusterer = hdbscan.HDBSCAN()
    # algorithm='best', alpha=1.0, approx_min_span_tree=True,
    # gen_min_span_tree=False,
    # metric='euclidean', min_cluster_size=2, min_samples=None, p=None)
clusterer.fit(usersMatrix)

clustering_results(clusterer.labels_,'HDBSCAN')
# print(clusterer.labels_)
#Mean Shift---------------------------------
bandwidth = estimate_bandwidth(usersMatrix, quantile=0.2)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(usersMatrix)

clustering_results(ms.labels_,'MeanShift')
#DBSCAN-------------------------------------
# for epsilon in range(150,600):
#     db = DBSCAN(eps=(epsilon+1)/1000, min_samples=5).fit(usersMatrix)
#     print((epsilon+1)/1000)
#     clustering_results(db.labels_,('DBSCAN'+str(epsilon)))
