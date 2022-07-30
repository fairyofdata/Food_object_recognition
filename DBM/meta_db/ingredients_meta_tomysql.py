import pymysql
import pandas as pd
from tqdm import tqdm

'''
식재료 메타 데이터 mysq에 적재
'''
data = pd.read_csv("./ingredients_meta.csv")
data = data.to_dict('records')

conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor() 
sql = "INSERT INTO ingredients_meta(ingredients, ingredients_code) VALUES(%s, %s)"

for record in tqdm(data):
    cursor.execute(sql, (record['ingredients'], record['ingredients_code']))
    conn.commit()    
cursor.close()
conn.close()


