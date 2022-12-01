# Forward alerts to Kafka
# Module: Kafka

import os
import logging
import sys
import json
from confluent_kafka.cimpl import Producer, Exception
from flask import Flask
from flask import request

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS', 'kafka:9092')
FLASK_SECRET_KEY  = os.getenv('FLASK_SECRET_KEY', 'changeKey')
KAFKA_TOPIC       = os.getenv('KAFKA_TOPIC', 'alertmanager-events')

# enable logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
    )
logger = logging.getLogger('alertmanager-kafka-forwarder')
logger.setFormatter(formatter)

# initialize the webservice
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
            logger.error("Failed to deliver message: {}".format(err))
        else:
            logger.info("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    try:
        content = json.loads(request.get_data())

        producer = Producer(kafka_config)
        producer.poll(0)

        for alert in content['alerts']:
            producer.produce(KAFKA_TOPIC, json.dumps(alert), callback=acked)

        producer.flush()
    except Exception as ex:
        logger.error("Exception happened: {}".format(ex))
        return "Alert FAILED", 501

    return "Alert OK", 200
