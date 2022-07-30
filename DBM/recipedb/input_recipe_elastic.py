import pandas as pd
from elasticsearch7 import Elasticsearch
from tqdm import tqdm

'''
elastic search doc 추가
'''
recipe_df = pd.read_csv("./dataextract/recipedb_csv/recipe10k_fdb.csv")
recipe_df = recipe_df.astype('str').astype({'recipe_code':'int'})
inputdata = recipe_df.to_dict("records")

es = Elasticsearch()

index_name = 'recipe_db'

for doc in tqdm(inputdata):     
    es.index(index=index_name, doc_type='_doc', body=doc)
es.indices.refresh(index=index_name)

