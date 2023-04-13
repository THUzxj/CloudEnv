import os
import time
import argparse
from datetime import datetime
import itertools

LABEL_DIR="labels"
WORKLOAD_CONFIGS=[
    {
        "user": 100 
    },
    {
        "user": 200
    },
    {
        "user": 300
    }
]

FAULT_DEVICES=[
    "br-ex", "tap59bf5233-ce", "tap81a0af59-a6", "tapa1131989-c0", # "veth236b2ec", "veth2f9a704"
]

# FAULT_TYPES=[
#     {
#         "type": "delay",
#         "values": ["0ms", "100ms", "500ms", "1000ms"],
#         "args": "20ms"
#     },
#     {
#         "type": "loss",
#         "values": ["0%", "5%", "10%", "15%", "30%"],
#         "args": "25%"
#     },
#     {
#         "type": "duplicate",
#         "values": ["0%", "10%"],
#         "args": ""
#     },
# ]

FAULT_TYPES=[
    {
        "type": "delay",
        "values": ["0ms", "500ms"],
        "args": "20ms"
    },
    {
        "type": "loss",
        "values": ["0%", "15%"],
        "args": "25%"
    },
    {
        "type": "duplicate",
        "values": ["0%"],
        "args": ""
    },
]

# PADDING_TIME=
# FAULT_TIMES=[10, 60, 300]
FAULT_TIMES = [60]

class Fault:
    def __init__(self, type, value, args):
        self.type = type
        self.value = value
        self.args = args
    
    def get_command(self):
        return f"{self.type} {self.value} {self.args}"

class FaultConfig:
    def __init__(self, dev, faults):
        self.dev = dev
        self.faults = faults

    def get_add_command(self):
        return f"tc qdisc add dev {self.dev} root netem {self.get_description()}"

    def get_del_command(self):
        return f"tc qdisc del dev {self.dev} root netem"

    def get_description(self):
        return ' '.join([fault.get_command() for fault in self.faults])

def generate_faults():
    faultGroups = []
    for fault in FAULT_TYPES:
        faultGroups.append([Fault(fault["type"], value, fault["args"]) for value in fault["values"]])

    return faultGroups

def getArgs():
    parser = argparse.ArgumentParser(description='Process args for retrieving arguments')
    parser.add_argument('-l', "--log", help="log file", required=True)
    parser.add_argument("-p", "--padding", help="padding_time (second)", required=True)
    parser.add_argument("-d", "--duations", help="fault injection duation (second)", required=True)

    return parser.parse_args()

if __name__ == "__main__":
    # if not os.path.exists(LABEL_DIR):
    #     os.mkdir(LABEL_DIR)

    # assert os.path.isdir(LABEL_DIR)
    args = getArgs()
    # must run in root
    assert os.getuid() == 0

    file = open(args.log, "a")

    faultGroups = generate_faults()

    fault_times = [int(duation) for duation in args.duations.split(',')]
    try:
        while True:
            for fiTime in fault_times:
                for dev in FAULT_DEVICES:
                    for faultSet in itertools.product(*faultGroups):
                        faultConfig = FaultConfig(dev, faultSet)
                        addCmd = faultConfig.get_add_command()
                        delCmd = faultConfig.get_del_command()
                        print(addCmd)
                        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {dev}, {faultConfig.get_description()}, start\n")
                        os.system(addCmd)
                        time.sleep(fiTime)
                        print(delCmd)
                        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {dev}, {faultConfig.get_description()}, stop\n")
                        file.flush()
                        os.system(delCmd)
                        time.sleep(int(args.padding))
    finally:
        for dev in FAULT_DEVICES:
            os.system(f"tc qdisc del dev {dev} root netem")
