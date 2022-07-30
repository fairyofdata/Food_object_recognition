import pymysql
import pandas as pd
from tqdm import tqdm

'''
레시피 메타 데이터 mysq에 적재
'''
data = pd.read_csv("./recipe_meta.csv")
data = data.to_dict('records')

conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor() 
sql = "INSERT INTO recipe_meta(recipe_nm, recipe_code) VALUES(%s, %s)"

for record in tqdm(data):
    cursor.execute(sql, [record['recipe_nm'], record['recipe_code']])
    conn.commit()    
cursor.close()
conn.close()
