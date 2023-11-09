from kafka import KafkaConsumer
import json
import pymysql
import pandas as pd
from functools import reduce
from datetime import datetime

RECIPEINFOTOPIC = "RECIPEINFO"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(RECIPEINFOTOPIC, bootstrap_servers=BROKERS)

#식재료 메타데이터 호출
conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor()

sql_meta = "SELECT * FROM ingredients_meta"
ingredients_meta_df = pd.read_sql(sql_meta, conn)
ingredients_meta_dic = dict(zip(ingredients_meta_df.ingredient, ingredients_meta_df.ingredient_code))

def comb2(offer_ingredients_code_list):
    '''
        유저가 제공할 수 있는 식재료 데이터 코드 조합 리스트 생성 함수
        ex. [2, 3, 5] -> [2, 3, 5, 2*3, 2*5, 3*5] -> [2, 3, 5, 6, 10, 15]
        :param
            offer_ingredients_code_list : 수 리스트
        :return
            조합한 후 생선된 리스트
    '''
    rslt = []
    for i in range(len(offer_ingredients_code_list)):
        for j in offer_ingredients_code_list[i + 1:]:
            rslt.append((offer_ingredients_code_list[i] * j))
    return offer_ingredients_code_list + rslt


#사용자가 교환을 희망할 시 사용될 교환데이터 적재
for message in consumer:
    msg = json.loads(message.value.decode())
    
    #사용자간 제공식재료, 필요식재료 매칭을 위해 코드화한 식재료를 일정단위로 각각 묶은 후 조합(제공식재료:1~2개, 필요식재료:전부)
    offer_ingredients_code_list = comb2(list(map(lambda x: ingredients_meta_dic[x], msg["ingredients"] + msg["basic_ingredients"])))
    for recipe in msg["searched_recipe_df"]:
        if recipe["pred"] != "lack":
            continue
        lack_ingredients_code = reduce(lambda x, y: x * y, list(map(lambda x: ingredients_meta_dic[x["lack_ingredients"]], recipe["lack_ingredients_link"])))
        for offer_ingredients_code in offer_ingredients_code_list:
            sql_ex = "INSERT INTO ex_ingredients_db(userid, offer_ingredients_code, lack_recipe_code, lack_ingredients_code, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            exdata = [msg["userid"], offer_ingredients_code, recipe["_source.recipe_code"], lack_ingredients_code, datetime.fromtimestamp(msg["timestamp"]), msg["latitude"], msg["longitude"]]
            cursor.execute(sql_ex, exdata)
            conn.commit()    
