import pymysql

storage_connect = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")
storage_cursor = storage_connect.cursor()

#user_input_db -> 사용자가 레시피 추천을 요청한 식재료 데이터 테이블 생성
sql2 = """ 
     CREATE TABLE user_input_db(
        userid VARCHAR(20) NOT NULL,
        ingredients VARCHAR(200) NOT NULL,
        basic_ingredients VARCHAR(200) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DECIMAL(16, 14) NOT NULL,
        longitude DECIMAL(17, 14) NOT NULL
 );
 """

#user_select_db -> 레시피 요청 후 열람한 레시피 데이터 테이블 생성
sql3 = """ 
    CREATE TABLE user_select_db(
        userid VARCHAR(20) NOT NULL,
        recipe_code INT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DECIMAL(16, 14) NOT NULL,
        longitude DECIMAL(17, 14) NOT NULL
);
"""

storage_cursor.execute(sql2) 
storage_cursor.execute(sql3) 

storage_connect.commit()
storage_connect.close()

