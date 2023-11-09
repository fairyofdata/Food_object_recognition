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

def search_recipe(ingredients_list, essential_ingredients_list, basic_ingredients_list, allergy_list):
    '''
        일반식재료, 필수식재료, 기본식재료, 알리지식재료를 기반으로 Search 하여 조리가능 레시피 추출 함수
        :param
            ingredients_list : 일반 기본식재료(객체 인식을 한 식재료)
            essential_ingredients_list : 필수 포함 식재료
            basic_ingredients_list : 기본식재료(조미료 등)
            allergy_list : 알러지 식재료
        :return
            요리가능한 레시피의 세부정보, 바로요리 가능한 요리 레시피, 재료가 1~2개 부족한 요리 레시피 
    '''
    #Elastic search 검색을 위한 데이터 포맷으로 변환
    ingredients_token = ' '.join(ingredients_list) if ingredients_list!=[''] else '없음'
    essential_ingredients_token = ' '.join(essential_ingredients_list) if essential_ingredients_list!=[''] else '없음'
    basic_ingredients_token = ' '.join(basic_ingredients_list) if basic_ingredients_list!=[''] else '없음'
    allergy_token = ' '.join(allergy_list) if allergy_list!=[''] else '없음'
    
    es = Elasticsearch()
    
    #식재료 타입별 must, must_not, filter를 활용한 검색 쿼리
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
    
    res = es.search(index="recipe_db", body=doc, size=1000)
    searched_recipe_df = json_normalize(res['hits']['hits'])

    #레시피별 요리가능 레벨에 따라 pred, lack, imp 값 부여 // lack의 경우 부족식재료 추가 삽입
    searched_recipe_df[["pred", "lack_ingredients"]] = searched_recipe_df["_source.ingredients_nm"].apply(lambda x : distribute_recipelevel(x, set(ingredients_list + essential_ingredients_list + basic_ingredients_list)))
    searched_recipe_df = searched_recipe_df[searched_recipe_df["pred"] != "imp"]
    
    #부족 식재료의 경우, 해당 식재료를 구매할 수 있는 링크 데이터 삽입
    searched_recipe_df["lack_ingredients_link"] = searched_recipe_df[searched_recipe_df["pred"] == "lack"]["lack_ingredients"].apply(lambda x : add_purchasing_links(x))
    
    searched_recipe_df = searched_recipe_df[["_source.recipe_code", "_source.recipe_nm", "_source.ingredients_nm", "_source.recipe_url", "_source.cooking_time", "_source.level_nm", "_source.qnt", "pred", "lack_ingredients_link", "_source.img_src"]]
    prep_recipe = list(searched_recipe_df[searched_recipe_df["pred"] == "pre"]["_source.recipe_nm"])
    lack_recipe = list(searched_recipe_df[searched_recipe_df["pred"] == "lack"]["_source.recipe_nm"])
    
    return searched_recipe_df, prep_recipe, lack_recipe

def distribute_recipelevel(recipe, ingredients_total_set):
    '''
        레시피별 바로가능, 조금부족, 불가능 구분하여 값을를 출력하는 함수
        :param
            recipe : 식재료 기반으로 검색된 레시피
        :return
            요리 가능 레벨에 따라 출력
    '''
    distribute_index = set(recipe.split(sep=', ')).difference(ingredients_total_set)
    if len(distribute_index) == 0:
        return pd.Series(["pre", None])
    elif len(distribute_index) <= 2:
        return pd.Series(["lack", list(distribute_index)])
    else:
        return pd.Series(["imp", None])
    
def add_purchasing_links(ingredients):
    '''
        조금부족 레시피의 식재료 구매링크 삽입 함수
        :param
            ingredients : 부족 식재료 레시피의 식재료
        :return
            이마트 SSG의 식재료 구매링크
    '''
    uris = []
    for ingredient in ingredients:
        uri = f"https://emart.ssg.com/search.ssg?target=all&query={ingredient}"
        uris.append({"lack_ingredients":ingredient, "link":uri})
    return uris

for message in consumer:
    msg = json.loads(message.value.decode())
    
    searched_recipe_df, prep_recipe, lack_recipe = search_recipe(msg["ingredients"], msg["essential_ingredients"], msg["basic_ingredients"], msg["allergy"])
    msg["searched_recipe_df"] = searched_recipe_df.to_dict('records')
    msg["prep_recipe"] = prep_recipe
    msg["lack_recipe"] = lack_recipe
    
    producer.send(RECIPEINFOTOPIC, json.dumps(msg).encode("utf-8"))
    
