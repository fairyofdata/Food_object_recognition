import pymysql


#서비스 간편 활용을 위한 user 데이터 저장(임시방편 시연용 코드)
local_connect = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
local_cursor = local_connect.cursor()

sql = """ 
    CREATE TABLE user_db(
        userid VARCHAR(20) NOT NULL,
        basic_ingredients VARCHAR(200) NOT NULL,
        allergy VARCHAR(200) NOT NULL
    );
"""

local_cursor.execute(sql)  
local_connect.commit()
local_connect.close()

sql_user = "INSERT INTO user_db(userid, basic_ingredients, allergy) VALUES (%s, %s, %s)"
userdata1 = ["KN", "설탕, 소금, 간장, 식초, 고추장, 통깨, 초장, 후추, 버터, 식용유, 참기름, 들기름, 다진마늘, 물엿, 맛술, 튀김가루, 마늘, 청양고추, 쪽파, 꿀, 김치", "아몬드, 사과"]
userdata2 = ["DH", "설탕, 소금, 간장, 식초, 고추장, 파슬리가루, 초장, 후추, 버터, 식용유, 참기름, 들기름, 다진마늘, 물엿, 맛술, 튀김가루, 마늘, 청양고추, 쪽파, 꿀", "복숭아, 밤"]

local_cursor.execute(sql_user, userdata1)
local_cursor.execute(sql_user, userdata2)
local_connect.commit()    

local_cursor.close()
local_connect.close()

















