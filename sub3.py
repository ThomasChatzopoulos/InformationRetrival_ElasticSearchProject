import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

movies = pd.read_csv('datasets/movies.csv') 
ratings = pd.read_csv('datasets/ratings.csv')

users = ratings.groupby('userId', as_index=False)['rating'].mean()

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(np.array(users['rating']).reshape(-1,1))

users = users.merge(pd.DataFrame(kmeans.labels_,columns=['cluster']),left_index=True, right_index=True)

ratings = ratings.merge(users[['userId','cluster']],left_on='userId',right_on='userId')
ratings = ratings.drop(columns=['timestamp'])

movies_on_ratings = ratings.sort_values(by='movieId').movieId.unique()

movies_mean_per_cluster = [pd.DataFrame()] * n_clusters
for i in range(n_clusters):
    movies_mean_per_cluster[i] = ratings.loc[(ratings['cluster'] == i)].groupby('movieId',as_index=True)['rating'].mean()

users_with_movies = ratings.groupby('userId', as_index=True)['movieId'].unique().apply(list)
movies_with_clusters = ratings.groupby('movieId', as_index=True)['cluster'].unique().apply(list)

userId_tail = []
movieId_tail = []
rating_tail = []

for user in users.userId:
    user_cluster = int(users.loc[(users['userId'] == user)]['cluster'])

    for movie in movies_on_ratings:
        if(user_cluster in movies_with_clusters[movie] and not movie in users_with_movies[user]): #<1s

            movie_rating = movies_mean_per_cluster[user_cluster][movie]
            userId_tail.append(user)
            movieId_tail.append(movie)
            rating_tail.append(movie_rating)

ratings_tail = pd.DataFrame({'userId':userId_tail,'movieId':movieId_tail,'rating':rating_tail,'cluster':[-1 for i in range(len(userId_tail))]})
ratings = ratings.append(ratings_tail,ignore_index=True)
print(ratings)
