from kafka import KafkaProducer, KafkaConsumer
from flask import Flask, request, jsonify
import json

#브라우저 통신
app = Flask(__name__)

INGREDIENTSTOPIC = "INGREDIENTS"
RECOMMANDTOPIC = "RECOMMAND"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

producer = KafkaProducer(bootstrap_servers=BROKERS)
consumer = KafkaConsumer(RECOMMANDTOPIC, bootstrap_servers=BROKERS)

#전달받은 식재료 데이터를 카프카로 전송하고 컨슈머로 송신 후 리턴
#해당부분은 "설계미스" -> 카프카로 보낼 시 순서 보장은 되나, 유저의 인터넷 상태에 의해 송신에러 발생 시, 데이터가 사라지지 않고 남아있어 데이터가 밀림
#레시피 추천을 받는 부분은 카프카를 들어내고 단순 연결필요(실습 및 활용 목적으로 적용 하였으나 큰 문제로 발생)
@app.route('/recipe_req/', methods = ['POST'])
def recipe_req():
    req_data = request.get_json()
    producer.send(INGREDIENTSTOPIC, json.dumps(req_data).encode("utf-8"))
    for message in consumer: 
        msg = json.loads(message.value.decode())
        break
    return jsonify(msg)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5003, debug=True) 
