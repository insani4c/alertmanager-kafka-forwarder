# Forward alerts to Kafka
# Module: Kafka

import json
from confluent_kafka.cimpl import Producer
from flask import Flask
from flask import request

app = Flask(__name__)
app.secret_key = 'changeKeyHeere'

# Yes need to have -, change it!
TOPIC = "outerrim-events"

# Authentication conf, change it!
kafka_config = {
    'bootstrap.servers': "kafka-1:19092,kafka-2:19093,kafka-3:19094",
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
        producer.produce(TOPIC, value=alert, callback=acked)

    producer.flush()
    return "Alert OK", 200
