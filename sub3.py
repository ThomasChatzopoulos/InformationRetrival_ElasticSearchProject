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

movies_mean_per_cluster = [pd.DataFrame()] * n_clusters
for i in range(n_clusters):
    movies_mean_per_cluster[i] = ratings.loc[(ratings['cluster'] == i)].groupby('movieId',as_index=True)['rating'].mean()
    # print(movies_mean_per_cluster[i])


clusters_with_movies = ratings.groupby('cluster', as_index=True)['movieId'].unique().apply(list)
# print(clusters_with_movies[0])
users_with_movies = ratings.groupby('userId', as_index=True)['movieId'].unique().apply(list)
# print(users_with_movies)
movies_with_clusters = ratings.groupby('movieId', as_index=True)['cluster'].unique().apply(list)
# print(movies_with_clusters)

# temp = pd.DataFrame([[1,1,1,-1]],columns=['userId','movieId','rating','cluster'])
userId_tail = []
movieId_tail = []
rating_tail = []
cur_user = 0

total_start_time = time.time()
for user in users.userId:
    user_cluster = int(users.loc[(users['userId'] == user)]['cluster'])
    # print(user_cluster)
    # print('---')
    # if(cur_user != user):
    #     print((user/671)*100,'%')
    #     cur_user = user
    # start_time = time.time()
    for movie in movies_on_ratings:
        # print(user,movie)
        if(user_cluster in movies_with_clusters[movie] and not movie in users_with_movies[user]): #<1s
        # if(True):
            # if(ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)].any().any()):
            # print(user,movie,user_cluster)
            # movie_rating = ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)]['rating'].mean() #8s
            movie_rating = movies_mean_per_cluster[user_cluster][movie]
            # movie_rating = 1
            # print(ratings.loc[(ratings['cluster'] == user_cluster) & (ratings['movieId'] == movie)]['rating'])
            # print(movie_rating)
            # temp = pd.DataFrame([[user,movie,movie_rating,-1]],columns=['userId','movieId','rating','cluster']) #4s
            userId_tail.append(user)
            movieId_tail.append(movie)
            rating_tail.append(movie_rating)
            # ratings_tail = ratings.append(temp,ignore_index=True) #11s
    # elapsed_time = time.time() - start_time
    # print(elapsed_time)

ratings_tail = pd.DataFrame({'userId':userId_tail,'movieId':movieId_tail,'rating':rating_tail,'cluster':[-1 for i in range(len(userId_tail))]})
ratings = ratings.append(ratings_tail,ignore_index=True)
print(ratings)
total_elapsed_time = time.time() - total_start_time
print(total_elapsed_time)