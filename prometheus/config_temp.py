# copy it to config.py
PROMETHEUS_URL = "http://127.0.0.1:9090"

EXPORTERS = [
    "node-exporter"
]

NODES = [
    {
        "ip": "192.168.1.1",
        "name": "openstack-manager"
    }
]

OUT_DIR = "data/"
