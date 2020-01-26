import math
import pandas as pd
from elasticsearch import Elasticsearch
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC

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

df_movies = pd.read_csv('datasets/movies.csv')
df_movies['genres'] = df_movies['genres'].apply(lambda x:x.split('|'))
mlb_df = pd.DataFrame(mlb.fit_transform(df_movies['genres']),columns=mlb.classes_,index=df_movies['genres'].index)
df_movies = df_movies.merge(mlb_df,left_index=True,right_index=True)

df_matrix = df_matrix.merge(df_movies,left_on='movieId',right_on='movieId')
df_matrix = df_matrix.drop(columns=['genres'])

df_ratings = pd.read_csv('datasets/ratings.csv',
                        usecols = ['userId', 'movieId', 'rating'], 
                        dtype = {'userId':'int64','movieId' : 'int64','rating':'float64'}
                        )

df_movies_rated = pd.DataFrame(df_ratings['movieId'].unique(),columns=['movieId'])
df_movies_rated = df_movies_rated.sort_values(by='movieId')
df_movies_rated = df_movies_rated.reset_index(drop=True)

df_matrix = df_matrix.merge(df_movies_rated,on='movieId',how='inner')
# for col in df_matrix.columns: 
#     print(col) 
# for _type in df_matrix.dtypes:
#     print(_type)

# # df_matrix.to_csv('mlvectors.csv')
# testing_user = df_ratings.loc[df_ratings['userId']==1]
# # print(testing_user)
# df_test = df_matrix.merge(testing_user,on='movieId',how='inner')
# # print(df_test)

# train_x = df_test.drop(columns=['rating','movieId','title'],axis=1)
# # print(train_x)
# for _type in train_x.dtypes:
#     print(_type)
# train_y = df_test['rating']
# # print(train_y)

# model = SVC()
# model.fit(train_x,train_y)

# predict_train = model.predict(train_x)
# # print('Target on train data',predict_train) 