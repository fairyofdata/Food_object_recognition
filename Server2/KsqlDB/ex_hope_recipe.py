from kafka import KafkaConsumer, KafkaProducer
import pymysql
from pymysql.cursors import DictCursor
import json
from decimal import *

EXINGREDIENTSTOPIC = "EXINGREDIENTS"
EXQUESTTOPIC = "EXREQUESTS"
BROKERS = ["localhost:9094"]

consumer = KafkaConsumer(EXINGREDIENTSTOPIC, bootstrap_servers=BROKERS)
producer = KafkaProducer(bootstrap_servers=BROKERS)

conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8", cursorclass=DictCursor)
cursor = conn.cursor()

'''
요청 데이터 -> 매칭 데이터
'''
def select_ex_recipe(msg):
    userid, ex_recipe_code = msg["userid"], msg["ex_recipe_code"]
    sql = f"SELECT * FROM ex_ingredients_db WHERE userid = '{userid}' and lack_recipe_code = '{ex_recipe_code}'"
    cursor.execute(sql)  
    ex_recipe_infos = cursor.fetchall()
    return ex_recipe_infos

'''
Decimal 데이터 인코더
'''
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

'''
매칭 데이터 KSQL로 데이터 전송
'''
for message in consumer:
    msg = json.loads(message.value.decode())
    ex_recipe_infos = select_ex_recipe(msg)
    for ex_recipe_info in ex_recipe_infos:
        ex_recipe_info["timestamp"] = msg["timestamp"]
        producer.send(EXQUESTTOPIC, json.dumps(ex_recipe_info, cls=DecimalEncoder).encode("utf-8"))
        
