from kafka import KafkaConsumer
import json
import pymysql
from datetime import datetime


INGREDIENTSTOPIC = "INGREDIENTS"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(INGREDIENTSTOPIC, bootstrap_servers=BROKERS)
conn = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")
cursor = conn.cursor()

'''
사용자 식재료 인식 데이터 적재
'''
for message in consumer:
    msg = json.loads(message.value.decode())
    sql = "INSERT INTO user_input_db(userid, ingredients, basic_ingredients, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)"
    userdata = [msg['userid'], str(msg['ingredients']+msg['essential_ingredients']), str(msg['basic_ingredients']), datetime.fromtimestamp(msg['timestamp']), msg['latitude'], msg['longitude']]
    cursor.execute(sql, userdata)   
    conn.commit()    
cursor.close()
conn.close()

