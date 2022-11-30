# alertmanager-kafka-forwarder

[![Docker Image CI](https://github.com/insani4c/alertmanager-kafka-forwarder/actions/workflows/docker-image.yml/badge.svg)](https://github.com/insani4c/alertmanager-kafka-forwarder/actions/workflows/docker-image.yml)

A Python daemon which receives alerts through [HTTP webhooks](https://prometheus.io/docs/alerting/configuration/#webhook-receiver-%3Cwebhook_config%3E) from [Prometheus' Alertmanager](https://github.com/prometheus/alertmanager) and forwards them to an [Kafka](https://kafka.apache.org/) topic.
