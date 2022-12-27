#!/bin/bash

apt install docker.io
docker run -d -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

wget https://grafana.com/api/dashboards/1860/revisions/29/download panel.json