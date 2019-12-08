from elasticsearch import helpers, Elasticsearch

#Elastic search must be active
#If the input is 'q' the loop is terminated

es = Elasticsearch()
query = input()

while(query!='q'):
    results = es.search(index="movies", body={"query": {"match": {'title':query}}})
    print(results)   
    query = input()
