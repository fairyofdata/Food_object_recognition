import pymysql

'''
메타데이터, 교환데이터 적재
'''
conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor()

sql1 = """ 
    CREATE TABLE ex_ingredients_db(
        userid VARCHAR(20) NOT NULL,
        offer_ingredients_code BIGINT NOT NULL,
        lack_recipe_code INT NOT NULL,
        lack_ingredients_code BIGINT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DECIMAL(16, 14) NOT NULL,
        longitude DECIMAL(17, 14) NOT NULL
    );
"""

sql2 = """ 
    CREATE TABLE ingredients_meta(
        ingredients VARCHAR(30) NOT NULL,
        ingredients_code INT NOT NULL
    );
"""

sql3 = """ 
    CREATE TABLE recipe_meta(
        recipe_nm VARCHAR(200) NOT NULL,
        recipe_code INT NOT NULL
    );
"""

cursor.execute(sql1)  
cursor.execute(sql2)  
cursor.execute(sql3)  
conn.commit()
conn.close()