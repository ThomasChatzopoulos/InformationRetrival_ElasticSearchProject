import csv
import codecs
from elasticsearch import helpers, Elasticsearch

es = Elasticsearch()

with open('datasets/movies.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='movies', doc_type='_doc')