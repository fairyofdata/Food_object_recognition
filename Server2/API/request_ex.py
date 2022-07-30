from kafka import KafkaProducer
from flask import Flask, request, jsonify
import json

'''
식재료 교환 요청 정보 수신
'''
app = Flask(__name__)

EXINGREDIENTSTOPIC = "EXINGREDIENTS"
BROKERS = ["localhost:9094"]
producer = KafkaProducer(bootstrap_servers=BROKERS)

@app.route('/ex_req/', methods = ['POST'])
def ex_req():
    req_data = request.get_json()
    producer.send(EXINGREDIENTSTOPIC, json.dumps(req_data).encode("utf-8"))
    return {"massge":"식재료 교환 요청 완료"}

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5004, debug=True) 
    