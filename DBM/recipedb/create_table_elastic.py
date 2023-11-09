from elasticsearch7 import Elasticsearch

#elastic search index 생성
es = Elasticsearch()

def make_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    print(es.indices.create(index=index_name))

index_name = 'recipe_db'
make_index(es, index_name) 



