import pymysql
import pandas as pd
from tqdm import tqdm


#식재료 이름과 고유코드 매칭 데이터 mysql에 적재
#ingredients, ingredients_code(Prime Number)

ingredients_meta = pd.read_csv("./ingredients_meta.csv")
ingredients_meta = ingredients_meta.to_dict('records')

local_connect = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
local_cursor = local_connect.cursor() 
sql = "INSERT INTO ingredients_meta(ingredient, ingredient_code) VALUES(%s, %s)"

for ingredient_meta in tqdm(ingredients_meta):
    local_cursor.execute(sql, (ingredient_meta['ingredient'], ingredient_meta['ingredient_code']))
    local_connect.commit()    
local_cursor.close()
local_connect.close()


