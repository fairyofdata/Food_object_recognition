from kafka import KafkaConsumer, KafkaProducer
from elasticsearch7 import Elasticsearch
from pandas.io.json import json_normalize
import json
import pandas as pd


INGREDIENTSTOPIC = "INGREDIENTS"
RECIPEINFOTOPIC = "RECIPEINFO"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(INGREDIENTSTOPIC, bootstrap_servers=BROKERS)
producer = KafkaProducer(bootstrap_servers=BROKERS)

'''
요리가능 레시피 검색(식재료 -> 레시피)
'''
def search_recipe(ingredients_list, essential_ingredients_list, basic_ingredients_list, allergy_list):
    
    ingredients_token = ' '.join(ingredients_list) if ingredients_list!=[''] else '없음'
    essential_ingredients_token = ' '.join(essential_ingredients_list) if essential_ingredients_list!=[''] else '없음'
    basic_ingredients_token = ' '.join(basic_ingredients_list) if basic_ingredients_list!=[''] else '없음'
    allergy_token = ' '.join(allergy_list) if allergy_list!=[''] else '없음'
    
    es = Elasticsearch()
    doc = {
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "ingredients_nm": {
                                        "query": ingredients_token,
                                        "operator": "or"
                                    }
                                },
                                "match": {
                                    "ingredients_nm": {
                                        "query": essential_ingredients_token,
                                        "operator": "and"
                                    }
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "match": {
                                    "ingredients_nm": {
                                        "query": allergy_token,
                                        "operator": "and"
                                    }
                                }
                            }                    
                        ],
                        "filter": [
                            {
                                "match": {
                                    "ingredients_nm": {
                                        "query": basic_ingredients_token,
                                        "operator": "or"
                                    }
                                }
                            }   
                        ]
                    }
                },
                "boost": "2", 
                "functions": [
                    {
                        "filter": { "match": { "ingredients_nm": ingredients_token } },
                        "weight": 4
                    }
                ],
                "max_boost": 4,
                "score_mode": "max",
                "boost_mode": "multiply",
                "min_score": 4    
            }
        }
    }
    res = es.search(index="recipe_db", body=doc, size=100)
    rep_df = json_normalize(res['hits']['hits'])
    
    '''
    바로가능, 조금부족, 불가능 구분
    '''
    def distributer(x):
        distribute_index = set(x.split(sep=', ')).difference(set(ingredients_list + essential_ingredients_list + basic_ingredients_list))
        if len(distribute_index) == 0:
            return pd.Series(["pre", None])
        elif len(distribute_index) <= 2:
            return pd.Series(["lack", list(distribute_index)])
        else:
            return pd.Series(["imp", None])
    
    '''
    조금부족 레시피 식재료 구매링크 삽입
    '''
    def addinfo(ingredients):
        uris = []
        for i in ingredients:
            uri = f"https://emart.ssg.com/search.ssg?target=all&query={i}"
            uris.append({"lack_ingredients":i, "link":uri})
        return uris

    rep_df[["pred", "lack_ingredients"]] = rep_df["_source.ingredients_nm"].apply(lambda x : distributer(x))
    rep_df = rep_df[rep_df["pred"] != "imp"]
    rep_df["lack_ingredients_link"] = rep_df[rep_df["pred"] == "lack"]["lack_ingredients"].apply(lambda x : addinfo(x))
    rep_df = rep_df[["_source.recipe_code", "_source.recipe_nm", "_source.ingredients_nm", "_source.recipe_url", "_source.cooking_time", "_source.level_nm", "_source.qnt", "pred", "lack_ingredients_link", "_source.img_src"]]
    prep_recipe = list(rep_df[rep_df["pred"] == "pre"]["_source.recipe_nm"])
    lack_recipe = list(rep_df[rep_df["pred"] == "lack"]["_source.recipe_nm"])
    return rep_df, prep_recipe, lack_recipe

for message in consumer:
    msg = json.loads(message.value.decode())
    rep_df, prep_recipe, lack_recipe = search_recipe(msg["ingredients"], msg["essential_ingredients"], msg["basic_ingredients"], msg["allergy"])
    msg["rep_df"] = rep_df.to_dict('records')
    msg["prep_recipe"] = prep_recipe
    msg["lack_recipe"] = lack_recipe
    producer.send(RECIPEINFOTOPIC, json.dumps(msg).encode("utf-8"))
    
