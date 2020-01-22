import pandas as pd
import numpy as np
import time
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
# print(movies)
ratings = pd.read_csv('datasets/ratings.csv')

users = ratings.groupby('userId', as_index=False)['rating'].mean()

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(np.array(users['rating']).reshape(-1,1))
# clustering_results(kmeans.labels_,'KMeans')
users = users.merge(pd.DataFrame(kmeans.labels_,columns=['cluster']),left_index=True, right_index=True)
# print(users)
ratings = ratings.merge(users[['userId','cluster']],left_on='userId',right_on='userId')
ratings = ratings.drop(columns=['timestamp'])
# print(ratings)
movies_on_ratings = ratings.sort_values(by='movieId').movieId.unique()
# print(movies_on_ratings)
cur_user = 0
for user in users.userId:
    user_cluster = int(users.loc[(users['userId'] == user)]['cluster'])
    # print(user_cluster)
    # print('---')
    if(cur_user != user):
        print((user/671)*100,'%')
        cur_user = user
    start_time = time.time()
    for movie in movies_on_ratings:
        # print(user,movie)
        if(ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)].any().any() and not ratings.loc[(ratings['userId'] == user) & (ratings['movieId'] == movie)].any().any()):
            # if(ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)].any().any()):
            # print(user,movie,user_cluster)
            movie_rating = ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)]['rating'].mean()
            # print(ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)]['rating'])
            # print(movie_rating)
            temp = pd.DataFrame([[user,movie,movie_rating,-1]],columns=['userId','movieId','rating','cluster'])
            ratings = ratings.append(temp,ignore_index=True)
    elapsed_time = time.time() - start_time
    print(elapsed_time)

print(ratings)