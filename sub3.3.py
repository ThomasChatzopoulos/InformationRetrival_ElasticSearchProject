import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

import plotly.express as px

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

movies = pd.read_csv('datasets/movies.csv') 
n_movies = movies['movieId'].size
print(n_movies)

ratings = pd.read_csv('datasets/ratings.csv')

ratings2 = ratings['movieId'].drop_duplicates()
print(len(ratings2.index))

users = ratings.groupby('userId', as_index=False)['rating'].mean()
# print(users)

for i in range(1,11):
    n_clusters = i
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(np.array(users['rating']).reshape(-1,1))
    # clustering_results(kmeans.labels_,'KMeans')

    users2 = ratings.groupby('userId', as_index=True)['movieId'].apply(list).reset_index(name='movies')
    users2['cluster'] = kmeans.labels_
    users3 = users2.groupby('cluster', as_index=True)['movies'].apply(lambda l: pd.Series([item for sublist in l for item in sublist]).unique()).reset_index(name='movies')

    flag = 0
    for item in users3['movies']:
        # print(item.size)
        if(item.size<n_movies):
            flag = 1 
    # print(i,flag)
