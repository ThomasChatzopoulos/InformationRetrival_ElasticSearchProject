from elasticsearch import helpers, Elasticsearch
import csv
import codecs
import json

es = Elasticsearch()

# query = input()

print(es.search(index="movies", body={"query": {"match": {'title':'GoldenEye (1995)'}}}))

# while(query!='q'):
#     print(search("http://localhost:9200/movies/_search",query))
#     query = input()





