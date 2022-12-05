# Forward alerts to Kafka
# Module: Kafka

import os
import logging
import sys
import json
from confluent_kafka.cimpl import Producer
from flask import Flask
from flask import request
from prometheus_client import Gauge, Summary, generate_latest

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS', 'kafka:9092')
FLASK_SECRET_KEY  = os.getenv('FLASK_SECRET_KEY', 'changeKey')
KAFKA_TOPIC       = os.getenv('KAFKA_TOPIC', 'alertmanager-events')

# enable logging to stdout
logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
    )
logger = logging.getLogger('alertmanager-kafka-forwarder')

# initialize the webservice
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

messages_produced_metric = Gauge('akf_messages_produced',
                                   'Messages Produced',
                                   ['name', 'partition']
                            )

post_alert_request_time_metric = Summary('akf_post_alert_request_processing_seconds', 
                                         'Time spent processing the alert'
                                 )

# kafka-config
kafka_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
}

@app.route('/alert', methods = ['POST'])
@post_alert_request_time_metric.time()
def postAlertManager():
    """Receive alerts and produce Kafka message"""

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):

        """Delivery report handler called on
        successful or failed delivery of message
        """

        if err is not None:
            logger.error("Failed to deliver message: %s", err)
        else:
            messages_produced_metric.labels(
                name=msg.topic(),
                partition=msg.partition()
            ).set(msg.offset())
            logger.info("Produced record to topic %s partition [%s] @ offset %s"
                  ,msg.topic(), msg.partition(), msg.offset())

    try:
        content = json.loads(request.get_data())

        producer = Producer(kafka_config)

        for alert in content['alerts']:
            producer.poll(0)
            producer.produce(KAFKA_TOPIC, json.dumps(alert), callback=acked)

        producer.flush()
    except Exception as ex:
        logger.error("Exception happened: %s", ex)
        return "Alert FAILED", 501

    return "Alert OK", 200

@app.route('/metrics')
def metrics():
    """Display Prometheus metrics"""

    return generate_latest()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default_req(path):
    """Serve all other requests"""

    return path, 200
