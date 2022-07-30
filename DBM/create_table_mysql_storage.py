import pymysql

conn = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")

cursor = conn.cursor()

'''
input데이터, select데이터 테이블 생성
'''

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

#user_select_db
sql3 = """ 
    CREATE TABLE user_select_db(
        userid VARCHAR(20) NOT NULL,
        recipe_code INT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DECIMAL(16, 14) NOT NULL,
        longitude DECIMAL(17, 14) NOT NULL
);
"""

cursor.execute(sql2) 
cursor.execute(sql3) 
conn.commit()
conn.close()

