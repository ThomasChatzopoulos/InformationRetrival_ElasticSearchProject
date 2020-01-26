import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch

def calc_mean(x):
    counter = sums = 0
    for i in x:
        if(not np.isnan(i)):
            counter += 1
            sums += i
    return sums/counter

es = Elasticsearch()

ratings = pd.read_csv('datasets/ratings.csv')
movies_mo = ratings.groupby('movieId', as_index=False)['rating'].mean()

while True:
    query = input('Write your query:')
    if(query == 'q'):
        break
    user_id = int(input('Write your id:'))
    metric_results = pd.DataFrame() 

    es_results = es.search(index="movies", body={"size":100,"query": {"match": {'title': query}}})

    df_es = pd.DataFrame(pd.DataFrame(es_results['hits']['hits'])[['_score','_source']])
    df_es_source = pd.DataFrame(list(df_es['_source']))
    df_es = df_es.merge(df_es_source,left_index=True,right_index=True)
    df_es = df_es.drop('_source',axis=1)
    df_es = df_es.rename(columns={'_score':'es_score'})
    scalar = 5/df_es['es_score'].max()
    df_es['es_score'] = df_es['es_score'].apply(lambda x:x*scalar)

    metric_results['movieId'] = df_es['movieId']
    metric_results['es_score'] = df_es['es_score']
    metric_results['movieId'] = metric_results['movieId'].apply(int)
    metric_results = metric_results.merge(movies_mo,left_on='movieId',right_on='movieId')
    metric_results = metric_results.rename(columns={'rating':'mo_rating'})
    metric_results = metric_results.merge(ratings[['movieId','rating']].loc[ratings['userId'] == user_id],left_on='movieId',right_on='movieId',how='left')
    metric_results['new_score'] = metric_results[['es_score', 'mo_rating','rating']].values.tolist()
    metric_results['new_score'] = metric_results['new_score'].apply(calc_mean)
    df_es_source['movieId'] = df_es_source['movieId'].apply(int)
    metric_results = metric_results.merge(df_es_source[['movieId','title']],left_on='movieId',right_on='movieId')
    print(metric_results[['title','new_score']].sort_values(by='new_score',ascending=False).to_string(index=False))
