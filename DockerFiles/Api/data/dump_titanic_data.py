ES_HOST = {
    "host" : "elastic", 
    "port" : 9200
}

INDEX_NAME = 'titanic'
TYPE_NAME = 'passenger'

ID_FIELD = 'passengerid'

import csv

import time

from elasticsearch import Elasticsearch

csv_input_file = open('test.csv')

csv_file_object = csv.reader(csv_input_file)
 
header = next(csv_file_object)
header = [item.lower() for item in header]

bulk_data = [] 

for row in csv_file_object:
    data_dict = {}
    for i in range(len(row)):
        data_dict[header[i]] = row[i]
    op_dict = {
        "index": {
            "_index": INDEX_NAME, 
            "_type": TYPE_NAME, 
            "_id": data_dict[ID_FIELD]
        }
    }
    bulk_data.append(op_dict)
    bulk_data.append(data_dict)

# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

def get_elastic_client():
    try:
        es.indices.exists('RANDOM')
    except Elasticsearch.exceptions.ConnectionError as error:
        print('Waiting for connection with ES')
        time.sleep(1)
        get_elastic_client()        

if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))

request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))


# bulk index the data
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
#print(" response: '%s'" % (res))


# sanity check
print("searching...")
res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
print(" response: '%s'" % (res))

print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])