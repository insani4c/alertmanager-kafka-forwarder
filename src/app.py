# Forward alerts to Kafka
# Module: Kafka

import os
import json
from confluent_kafka.cimpl import Producer
from flask import Flask
from flask import request

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS', 'kafka:9092')
FLASK_SECRET_KEY  = os.getenv('FLASK_SECRET_KEY', 'changeKey')
KAFKA_TOPIC       = os.getenv('KAFKA_TOPIC', 'alertmanager-events')

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# kafka-config
kafka_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
}

@app.route('/alert', methods = ['POST'])
def postAlertManager():

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):

        """Delivery report handler called on
        successful or failed delivery of message
        """

        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    producer = Producer(kafka_config)
    content = json.loads(request.get_data())

    for alert in content['alerts']:
        producer.poll(0)
        producer.produce(KAFKA_TOPIC, json.dumps(alert), callback=acked)

    producer.flush()
    return "Alert OK", 200
