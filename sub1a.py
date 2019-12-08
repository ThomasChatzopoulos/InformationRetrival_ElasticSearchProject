from elasticsearch import helpers, Elasticsearch
import csv
import codecs

es = Elasticsearch()

with open('movies.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='movies', doc_type='_doc')