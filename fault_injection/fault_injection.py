import argparse
import socket
import itertools
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description='Process args for retrieving arguments')

    # log file
    parser.add_argument('-l', "--log", help="log file", required=True)

    # schedule
    parser.add_argument("-p", "--padding", help="padding_time (second)", required=True)
    parser.add_argument("-d", "--duations", help="fault injection duation (second)", required=True)

    parser.add_argument("--dry", )
    return parser.parse_args()

interfaces = [iface[1] for iface in socket.if_nameindex()]

cartesian_product = list(itertools.product(interfaces))

FAULTS = [
    {
        "type": "delay",
        "values": [0, 500],
        "unit": "ms",
        "args": "20ms"
    },
    {
        "type": "loss",
        "values": [0, 15],
        "unit": "%",
        "args": "25%"
    },
    {
        "type": "duplicate",
        "values": [0],
        "unit": "%",
        "args": ""
    }
]


def log(logfile, event, cmd):
    with open(logfile, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{event}, {cmd}")

for 

