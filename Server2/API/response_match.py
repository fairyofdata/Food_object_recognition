from kafka import KafkaConsumer
import json
import requests

#미완성
#브라우저로 식재료 교환 매칭 정보 송신
#데이터를 전송할 유저 IP 주소값 필요
#메일 전송 프로토콜을 활용 하여 데이터 전송 구현 계획
MATCHTOPIC = "MATCHUSER"
BROKERS = ["localhost:9094"]

consumer = KafkaConsumer(MATCHTOPIC, bootstrap_servers=BROKERS)

for message in consumer:
    msg = json.loads(message.value.decode())
    requests.post('http://localhost:5001/ex_res/', json=msg)

