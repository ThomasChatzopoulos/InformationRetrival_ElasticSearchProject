import pandas as pd
from elasticsearch import helpers, Elasticsearch

es = Elasticsearch()

while True:
    query = input('Write your query:')
    if(query == 'q'):
        break
    
    es_results = es.search(index="movies", body={"size":100,"query": {"match": {'title': query}}})
    # print(es_results)

    df_es = pd.DataFrame(pd.DataFrame(es_results['hits']['hits'])[['_score','_source']])
    df_es_source = pd.DataFrame(list(df_es['_source']))
    df_es = df_es.merge(df_es_source,left_index=True,right_index=True)
    df_es = df_es.drop('_source',axis=1)
    df_es = df_es.rename(columns={'_score':'es_score'})
    print(df_es)