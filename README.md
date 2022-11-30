# alertmanager-kafka-forwarder

[![Docker Image CI](https://github.com/insani4c/alertmanager-kafka-forwarder/actions/workflows/docker-image.yml/badge.svg)](https://github.com/insani4c/alertmanager-kafka-forwarder/actions/workflows/docker-image.yml)

A Python daemon which receives alerts through [HTTP webhooks](https://prometheus.io/docs/alerting/configuration/#webhook-receiver-%3Cwebhook_config%3E) from [Prometheus' Alertmanager](https://github.com/prometheus/alertmanager) and forwards them to an [Kafka](https://kafka.apache.org/) topic.

## Example

Docker Compose Example:

```docker
  alertmanager-kafka-forwarder: 
    image: ghcr.io/insani4c/alertmanager-kafka-forwarder:main
    container_name: alertmanager-kafka-forwarder
    environment:
        BOOTSTRAP_SERVERS: "kafka-1:9092,kafka-2:9092"
        FLASK_SECRET_KEY: "mySecretKey"
        KAFKA_TOPIC: "alertmanager-events"
    ports:
      - 9792:9792

```
