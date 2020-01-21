import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def clustering_results(resultMatrix,algorithmName):
    print('---',algorithmName,'---')
    labels_unique = np.unique(resultMatrix)
    minValue = min(resultMatrix)
    n_clusters = len(labels_unique)
    print('Number of clusters:',n_clusters)
    clusters = [0] * (n_clusters)
    print('min:',minValue)
    for value in resultMatrix:
        clusters[value-minValue] += 1
    print('Clusters population:',clusters)

movies = pd.read_csv('datasets/movies.csv') 

ratings = pd.read_csv('datasets/ratings.csv')

users = ratings.groupby('userId', as_index=False)['rating'].mean()

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(np.array(users['rating']).reshape(-1,1))
clustering_results(kmeans.labels_,'KMeans')






