import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

#This script takes some time to complete due to large input data and metadata produced
#Average time 2min depending on host machine 

movies = pd.read_csv('datasets/movies.csv') 
ratings = pd.read_csv('datasets/ratings.csv')

users = ratings.groupby('userId', as_index=False)['rating'].mean() #Average rating per user

n_clusters = 3 #The optimal clusters is 2 for this input but 3 is used instead for better results and faster calculations
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(np.array(users['rating']).reshape(-1,1))

users = users.merge(pd.DataFrame(kmeans.labels_,columns=['cluster']),left_index=True, right_index=True) #Add cluster labels to users

ratings = ratings.merge(users[['userId','cluster']],left_on='userId',right_on='userId') #Add cluster labels to ratings
ratings = ratings.drop(columns=['timestamp'])

movies_on_ratings = ratings.sort_values(by='movieId').movieId.unique() #All movies that have been rated

#Calculate the mean of every movie for every cluster
movies_mean_per_cluster = [pd.DataFrame()] * n_clusters 
for i in range(n_clusters):
    movies_mean_per_cluster[i] = ratings.loc[(ratings['cluster'] == i)].groupby('movieId',as_index=True)['rating'].mean()

#All users with a list of movies rated for each
users_with_movies = ratings.groupby('userId', as_index=True)['movieId'].unique().apply(list)
#All movies with a list of clusters they belong
movies_with_clusters = ratings.groupby('movieId', as_index=True)['cluster'].unique().apply(list)

userId_tail = []
movieId_tail = []
rating_tail = []

for user in users.userId:
    user_cluster = int(users.loc[(users['userId'] == user)]['cluster'])

    for movie in movies_on_ratings:
        #Check if movie belongs to user's cluster and has not been rated by him
        if(user_cluster in movies_with_clusters[movie] and not movie in users_with_movies[user]): 

            movie_rating = movies_mean_per_cluster[user_cluster][movie]
            userId_tail.append(user)
            movieId_tail.append(movie)
            rating_tail.append(movie_rating)

ratings_tail = pd.DataFrame({'userId':userId_tail,'movieId':movieId_tail,'rating':rating_tail,'cluster':[-1 for i in range(len(userId_tail))]})
ratings = ratings.append(ratings_tail,ignore_index=True) #Add produced rating data to existing
print(ratings)
ratings.to_csv('datasets/ratings.csv',index=False)
