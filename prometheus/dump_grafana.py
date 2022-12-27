import json

import argparse
from datetime import datetime
from datetime import timedelta
import os
from prometheus_pandas import query
import math
from config import PROMETHEUS_URL, EXPORTERS, NODES, OUT_DIR

def load_targets():
    fi = open("panel.json")
    data = json.load(fi)

    allTargets = []
    for panel in data["panels"]:
        print("title", panel["title"])
        if ("description" in panel):
            print(panel["description"])
        if ("panels" in panel):
            for subpanel in panel["panels"]:
                print("subpanel title:", subpanel["title"])
                for i, target in enumerate(subpanel["targets"]):
                    if "expr" in target:
                        # print(target)
                        allTargets.append({
                            "expr": target["expr"],
                            "format": target.get("format", ""),
                            "legendFormat": target.get("legendFormat", ""),
                            "title": panel["title"] + "__" + subpanel["title"] + "__" + str(i)
                        })
        for i, target in enumerate(panel["targets"]):
            if "expr" in target:
                # print(target)
                allTargets.append({
                    "expr": target["expr"],
                    "format": target.get("format", ""),
                    "legendFormat": target.get("legendFormat", ""),
                    "title": panel["title"]+ "__" + str(i)
                })
    return allTargets

def dump_targets(allTargets):
    fo = open("targets.txt", "w")
    for target in allTargets:
        fo.write(",".join(list(target.values()))+"\n")

def get_target_dict(allTargets):
    dictTarget = {}
    for target in allTargets:
        targetId = target["title"]
        if targetId in dictTarget:
            raise Exception("Conflict targetId", targetId)
        dictTarget[targetId] = target
    return dictTarget

def getArgs():
    parser = argparse.ArgumentParser(description='Process args for retrieving arguments')
    
    parser.add_argument('-s', "--start", help="query start time", required=True)
    parser.add_argument('-e', "--end", help="query end time", required=True)
    parser.add_argument('-S', "--step", help="step", required=True)
    parser.add_argument('-o', "--out", help="out dir")
    parser.add_argument('-b', '--batch', help="store batch (hour)", default=24)

    return parser.parse_args()

def dump_prometheus_data_multiple_periods(output_folder, q, start_times, end_times, steps, batch):
    """ Loads data from a PromQL-compatible datasource

    :param output_folder: The path to the output folder

    """
    p = query.Prometheus(PROMETHEUS_URL)
    for i in range(len(start_times)):
        # split into hourly samples
        start_date = datetime.strptime(start_times[i], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_times[i], "%Y-%m-%d %H:%M:%S")
        duration = end_date - start_date
        seconds = duration.total_seconds()
        hours = math.ceil(seconds/(3600*batch))
        # Request the data from prometheus
        tf_start = start_date
        for j in range(hours):
            print(q)
            tf_end = tf_start + timedelta(hours=batch)
            if tf_end > end_date:
                tf_end = end_date
            ts = p.query_range(query=q, start=tf_start, end=tf_end, step=steps[i])
            tf_start = tf_end
            file_name = os.path.join(output_folder, "ts_" + str(j) + ".csv")
            if ts.empty:
                continue
            os.makedirs(output_folder, exist_ok=True)
            ts.to_csv(file_name)
    return


if __name__ == "__main__":
    args = getArgs()
    allTargets = load_targets()

    if(os.path.exists(args.out)):
        raise Exception(f"{args.out} already exists")

    for node in NODES:
        for target in allTargets:
            out_path = os.path.join(args.out, node["name"].replace("/", "-"), target["title"].replace("/", "-")) 
            expr = target["expr"].replace("$node", f"{node['ip']}:9100").replace("$job", "prometheus").replace("$__rate_interval", "1m0s")
            dump_prometheus_data_multiple_periods(out_path, expr, [args.start], [args.end], [args.step], args.batch)
