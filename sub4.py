import math
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn import preprocessing

#This script takes a lot of time to complete
#Average time to complete all 671 users is about 11hours (1min per user) depending on host machine

def extract_tf_idf(dictionary,n_documents): #tf-idf calculator
    for term in dictionary:
        tf = dictionary[term]['term_freq']/len(dictionary)
        idf = math.log(n_documents/dictionary[term]['doc_freq'],10)
        dictionary[term] = tf*idf
    return dictionary

es = Elasticsearch()
mlb = MultiLabelBinarizer()
lab_enc = preprocessing.LabelEncoder()

array = []
result = es.search(index="movies", body={"size":10000, "query": {"match_all": {}}})     
for res in result['hits']['hits']:
    array.append([res['_id'], res['_source']['movieId']])

id_match = pd.DataFrame(array, columns=['es_id','movieId']) #Match between elasticsearch id and movie id

#Get term vectors from elasticsearch
es_vectors = []
for doc in es.mtermvectors(index="movies", doc_type="_doc", body=dict(ids=list(id_match.es_id), parameters=dict(term_statistics=True, field_statistics=False, fields=["title"])))['docs']:
    es_vectors.append([doc['_id'], doc['term_vectors']['title']['terms']])

#Term vector preprocessing
df_es_vectors = pd.DataFrame(es_vectors, columns=['es_id', 'terms_vector'])
#Calculate tf-idf
df_es_vectors['terms_vector'] = df_es_vectors['terms_vector'].apply(lambda x: extract_tf_idf(x, len(df_es_vectors.index)))
df_es_vectors = df_es_vectors.merge(id_match, left_on='es_id', right_on='es_id')
df_es_vectors = df_es_vectors.drop(columns=['es_id'])
df_es_vectors = df_es_vectors[['movieId', 'terms_vector']]
tf_idf_matrix = df_es_vectors['terms_vector'].apply(pd.Series)
tf_idf_matrix = tf_idf_matrix.fillna(0)
df_es_vectors = df_es_vectors.merge(tf_idf_matrix, left_index=True, right_index=True)
df_matrix = df_es_vectors.drop(columns=['terms_vector'])
df_matrix['movieId'] = df_matrix['movieId'].apply(int)
df_matrix = df_matrix.sort_values(by='movieId')
df_matrix = df_matrix.reset_index(drop=True)

#Movies preprocessing
df_movies = pd.read_csv('datasets/movies.csv', usecols = ['movieId', 'genres'])
movie_ids = df_movies['movieId'].unique()
df_movies['genres'] = df_movies['genres'].apply(lambda x:x.split('|'))
mlb_df = pd.DataFrame(mlb.fit_transform(df_movies['genres']), columns=mlb.classes_, index=df_movies['genres'].index)
mlb_df = mlb_df.drop(columns='(no genres listed)')
mlb_df = mlb_df.add_suffix('_genre')
df_movies = df_movies.merge(mlb_df,left_index=True,right_index=True)

df_matrix = df_matrix.merge(df_movies,left_on='movieId',right_on='movieId')
df_matrix = df_matrix.drop(columns=['genres'])

df_ratings = pd.read_csv('datasets/ratings.csv',
                         usecols = ['userId', 'movieId', 'rating'], 
                         dtype = {'userId':'int64', 'movieId' : 'int64', 'rating':'float64'}
                        )
df_ratings = df_ratings.rename(columns={"rating": "user_rating"})

users_ids = df_ratings['userId'].unique()

users_with_movies = df_ratings.groupby('userId', as_index=True)['movieId'].unique().apply(list)

userId_tail = []
movieId_tail = []
rating_tail = []

df_matrix = df_matrix.set_index('movieId')

for userId in users_ids: #For every user
    df_user = df_ratings.loc[df_ratings['userId'] == userId] #Get all user's ratings
    df_user = df_user.set_index('movieId')
    df_train = df_matrix.merge(df_user, right_index=True, left_index=True, how='inner')
    train_x = df_train.drop(columns=['user_rating', 'userId'], axis=1)
    scaler = preprocessing.StandardScaler()
    scaler.fit(train_x) #Normalize values arround 0
    train_x = scaler.transform(train_x)
    train_y = df_train['user_rating'] #Labels
    train_y = lab_enc.fit_transform(train_y)
    train_y = train_y.astype('int')
    lsvc = LinearSVC(class_weight='balanced', max_iter=500)
    lsvc.fit(train_x, train_y) #Train model
    print(userId)
    for movie in movie_ids: #For every movie not rated by the user
        if not movie in users_with_movies[userId]:
            userId_tail.append(userId)
            movieId_tail.append(movie)
            predict_x = np.array(df_matrix.loc[movie, :]).reshape(1, -1)
            ml_rating = lsvc.predict(predict_x)
            rating_tail.append(ml_rating)

ratings_tail = pd.DataFrame({'userId':userId_tail, 'movieId':movieId_tail, 'rating':rating_tail})
print(ratings_tail)
