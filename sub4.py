import math
import pandas as pd
from elasticsearch import Elasticsearch
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn import utils
from sklearn.metrics import accuracy_score

def extract_tf_idf(dictionary,n_documents):
    for term in dictionary:
        tf = dictionary[term]['term_freq']/len(dictionary)
        idf = math.log(n_documents/dictionary[term]['doc_freq'],10)
        dictionary[term] = tf*idf
    return dictionary

es = Elasticsearch()

array = []
result = es.search(index="movies", body={"size":10000,"query": {"match_all": {}}})     
for res in result['hits']['hits']:
    array.append([res['_id'],res['_source']['movieId']])

id_match = pd.DataFrame(array,columns=['es_id','movieId'])

pairs = []
for doc in es.mtermvectors(index="movies",doc_type="_doc",body=dict(ids=list(id_match.es_id),parameters=dict(term_statistics=True,field_statistics=False,fields=["title"])))['docs']:
    pairs.append([doc['_id'],doc['term_vectors']['title']['terms']])

df_pairs = pd.DataFrame(pairs,columns=['es_id','terms_vector'])
df_pairs['terms_vector'] = df_pairs['terms_vector'].apply(lambda x: extract_tf_idf(x,len(df_pairs.index)))
df_pairs = df_pairs.merge(id_match,left_on='es_id',right_on='es_id')
df_pairs = df_pairs.drop(columns=['es_id'])
df_pairs = df_pairs[['movieId','terms_vector']]
tf_idf_matrix = df_pairs['terms_vector'].apply(pd.Series)
tf_idf_matrix = tf_idf_matrix.fillna(0)
df_pairs = df_pairs.merge(tf_idf_matrix,left_index=True,right_index=True)
df_matrix = df_pairs.drop(columns=['terms_vector'])
df_matrix['movieId'] = df_matrix['movieId'].apply(int)
df_matrix = df_matrix.sort_values(by='movieId')
df_matrix = df_matrix.reset_index(drop=True)

mlb = MultiLabelBinarizer()

df_movies = pd.read_csv('datasets/movies.csv',usecols = ['movieId', 'genres'])
df_movies['genres'] = df_movies['genres'].apply(lambda x:x.split('|'))
mlb_df = pd.DataFrame(mlb.fit_transform(df_movies['genres']),columns=mlb.classes_,index=df_movies['genres'].index)
mlb_df = mlb_df.drop(columns='(no genres listed)')
mlb_df = mlb_df.add_suffix('_genre')
df_movies = df_movies.merge(mlb_df,left_index=True,right_index=True)

df_matrix = df_matrix.merge(df_movies,left_on='movieId',right_on='movieId')
df_matrix = df_matrix.drop(columns=['genres'])

df_ratings = pd.read_csv('datasets/ratings.csv',
                        usecols = ['userId', 'movieId', 'rating'], 
                        dtype = {'userId':'int64','movieId' : 'int64','rating':'float64'}
                        )
df_ratings = df_ratings.rename(columns={"rating": "user_rating"})
df_movies_rated = pd.DataFrame(df_ratings['movieId'].unique(),columns=['movieId'])
df_movies_rated = df_movies_rated.sort_values(by='movieId')
df_movies_rated = df_movies_rated.reset_index(drop=True)

df_matrix = df_matrix.merge(df_movies_rated,on='movieId',how='inner')

lab_enc = preprocessing.LabelEncoder()

users_ids = df_ratings['userId'].unique()

user = df_ratings.loc[df_ratings['userId']==2]
df_test = df_matrix.merge(user,on='movieId',how='inner')
for name in df_test:
    columnsum = df_test[name].sum()
    if(columnsum == 0):
        df_test = df_test.drop(columns=[name])
df_test.to_csv('mltesting.csv',index=False)

# print(user)
# print(users_ids)
# for i in users_ids:
#     user = df_ratings.loc[df_ratings['userId']==i]
#     df_test = df_matrix.merge(user,on='movieId',how='inner')
#     train_x = df_test.drop(columns=['rating','movieId','title'],axis=1)
#     train_x = train_x.apply(lambda x:x*10)
#     train_y = df_test['rating']
#     train_y['rating'] = train_y['rating'].apply(lambda x:x*10)
#     training_scores_encoded = lab_enc.fit_transform(train_y)
#     train_y = train_y.astype('int')
#     model = SVC()
#     model.fit(train_x,train_y)
#     predict_train = model.predict(train_x)
#     print(i,training_scores_encoded)
#     print(i,predict_train) 
#     accuracy_train = accuracy_score(train_y,predict_train)
#     print(i,'accuracy_score on train dataset : ' ,accuracy_train)