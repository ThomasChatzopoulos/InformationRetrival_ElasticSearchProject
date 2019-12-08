from elasticsearch import helpers, Elasticsearch
import csv
import codecs
import requests
import json


#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

res = requests.get('http://localhost:9200')
print(res.content)
def search(uri, term):
    query = json.dumps({
        "query": {
            "match all": {}
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results

# es = Elasticsearch()

query = input()

while(query!='q'):
    print(search("http://localhost:9200/movies/_search",query))
    query = input()





