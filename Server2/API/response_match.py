from kafka import KafkaConsumer
import json
import requests

#미완성
'''
식재료 교환 매칭 정보 송신
'''
MATCHTOPIC = "MATCHUSER"
BROKERS = ["localhost:9094"]

consumer = KafkaConsumer(MATCHTOPIC, bootstrap_servers=BROKERS)

for message in consumer:
    msg = json.loads(message.value.decode())
    requests.post('http://localhost:5001/ex_res/', json=msg)

