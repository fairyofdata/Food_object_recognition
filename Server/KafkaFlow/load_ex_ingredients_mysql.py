from kafka import KafkaConsumer
import json
import pymysql
import pandas as pd
from functools import reduce
from datetime import datetime

RECIPEINFOTOPIC = "RECIPEINFO"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(RECIPEINFOTOPIC, bootstrap_servers=BROKERS)

'''
식재료 메타데이터 호출
'''
conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor()

sql_meta = "SELECT * FROM ingredients_meta"
ingredients_meta_df = pd.read_sql(sql_meta, conn)
ingredients_meta_dic = dict(zip(ingredients_meta_df.ingredients, ingredients_meta_df.ingredients_code))

'''
식재료 코드화
'''
def comb2(arr):
    rslt = []
    for i in range(len(arr)):
        for j in arr[i + 1:]:
            rslt.append((arr[i] * j))
    return arr + rslt

'''
사용자 교환데이터 적재
'''                
for message in consumer:
    msg = json.loads(message.value.decode())
    offer_ingredients_code_list = comb2(list(map(lambda x: ingredients_meta_dic[x], msg["ingredients"] + msg["basic_ingredients"])))
    for recipe in msg["rep_df"]:
        if recipe["pred"] != "lack":
            continue
        lack_ingredients_code = reduce(lambda x, y: x * y, list(map(lambda x: ingredients_meta_dic[x["lack_ingredients"]], recipe["lack_ingredients_link"])))
        for oic in offer_ingredients_code_list:
            sql_ex = "INSERT INTO ex_ingredients_db(userid, offer_ingredients_code, lack_recipe_code, lack_ingredients_code, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            exdata = [msg["userid"], oic, recipe["_source.recipe_code"], lack_ingredients_code, datetime.fromtimestamp(msg["timestamp"]), msg["latitude"], msg["longitude"]]
            cursor.execute(sql_ex, exdata)
            conn.commit()    
cursor.close()
conn.close()
