from kafka import KafkaProducer, KafkaConsumer
from flask import Flask, request, jsonify
import json

'''브라우저 통신'''
app = Flask(__name__)

INGREDIENTSTOPIC = "INGREDIENTS"
RECOMMANDTOPIC = "RECOMMAND"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

producer = KafkaProducer(bootstrap_servers=BROKERS)
consumer = KafkaConsumer(RECOMMANDTOPIC, bootstrap_servers=BROKERS)

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
