import pymysql


#메타데이터,식재료 교환데이터 테이블 생성
conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor()

#식재료 교환 서비스 데이터 저장 테이블 생성
sql1 = """ 
    CREATE TABLE ex_ingredient_db(
        userid VARCHAR(20) NOT NULL,
        offer_ingredients_code BIGINT NOT NULL,
        lack_recipe_code INT NOT NULL,
        lack_ingredients_code BIGINT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DECIMAL(16, 14) NOT NULL,
        longitude DECIMAL(17, 14) NOT NULL
    );
"""

#식재료 메타 데이터 테이블 생성
sql2 = """ 
    CREATE TABLE ingredient_meta(
        ingredient VARCHAR(30) NOT NULL,
        ingredient_code INT NOT NULL
    );
"""

#레시피 메타 데이터 테이블 생성
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