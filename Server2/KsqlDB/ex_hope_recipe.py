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

local_connect = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8", cursorclass=DictCursor)
locla_cursor = local_connect.cursor()

def select_ex_recipe(msg):
    '''
        유저가 특정 부족식재료 레시피의 식재료를 교환 요청 했을 시, 적재되어 있는 매칭 가능한 형태의 테이터로 교환
        :param
            msg : 교환요청 유저,레시피,식재료 데이터
        :return
            MySQL에 적재해논 데이터 가져온 후 리턴
            /KDT_FinalProject_1/Server/KafkaFlow/load_ex_ingredients_mysql.py 참고
    '''
    userid, ex_recipe_code = msg["userid"], msg["ex_recipe_code"]
    sql = f"SELECT * FROM ex_ingredients_db WHERE userid = '{userid}' and lack_recipe_code = '{ex_recipe_code}'"
    locla_cursor.execute(sql)  
    ex_recipe_infos = locla_cursor.fetchall()
    return ex_recipe_infos


#Decimal 데이터 인코더
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


for message in consumer:
    msg = json.loads(message.value.decode())
    
    #요청데이터를 매칭데이터로 교환
    ex_recipe_infos = select_ex_recipe(msg)
    
    #매칭 데이터 KSQL로 데이터 전송
    for ex_recipe_info in ex_recipe_infos:
        ex_recipe_info["timestamp"] = msg["timestamp"]
        producer.send(EXQUESTTOPIC, json.dumps(ex_recipe_info, cls=DecimalEncoder).encode("utf-8"))
        
