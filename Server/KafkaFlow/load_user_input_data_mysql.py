from kafka import KafkaConsumer
import json
import pymysql
from datetime import datetime


INGREDIENTSTOPIC = "INGREDIENTS"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(INGREDIENTSTOPIC, bootstrap_servers=BROKERS)
storage_connect = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")
storage_cursor = storage_connect.cursor()

#user_input_db -> 사용자가 레시피 추천을 요청한 식재료 데이터 적재 // 향후 데이터 분석 시 활용
for message in consumer:
    msg = json.loads(message.value.decode())
    
    sql = "INSERT INTO user_input_db(userid, ingredients, basic_ingredients, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)"
    userdata = [msg['userid'], str(msg['ingredients']+msg['essential_ingredients']), str(msg['basic_ingredients']), datetime.fromtimestamp(msg['timestamp']), msg['latitude'], msg['longitude']]
    storage_cursor.execute(sql, userdata)   
    storage_connect.commit()    

