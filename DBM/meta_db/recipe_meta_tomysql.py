import pymysql
import pandas as pd
from tqdm import tqdm


#레시피 이름과 고유코드 매칭 데이터 mysql에 적재
#recipe, recipe_code(Prime Number)

recipes_meta = pd.read_csv("./recipes_meta.csv")
recipes_meta = recipes_meta.to_dict('records')

local_connent = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
local_cursor = local_connent.cursor() 
sql = "INSERT INTO recipes_meta(recipe_nm, recipe_code) VALUES(%s, %s)"

for recipe_meta in tqdm(recipes_meta):
    local_cursor.execute(sql, [recipe_meta['recipe_nm'], recipe_meta['recipe_code']])
    local_connent.commit()    
local_cursor.close()
local_connent.close()
