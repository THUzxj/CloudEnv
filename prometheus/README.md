# Grafana

[panel json](https://grafana.com/api/dashboards/1860/revisions/29/download)

(Grafana)[https://grafana.com/grafana/download]

(Prometheus in Grafana)[https://prometheus.io/docs/visualization/grafana/]

The url is the ip of the host. (When using docker)

(Dashboard)[https://grafana.com/grafana/dashboards/1860-node-exporter-full/]

# Prometheus

Running on the host

Port: 9090

# Exporters

## Node

```bash
apt install prometheus-node-exporter
```

port: 9100

## libvirt


port: 9177

# Troubleshooting

## Permission denied on accessing host directory in Docker

```bash
chown :100 /example
chmod 777 /example
```

## Partial panels show "no data"

