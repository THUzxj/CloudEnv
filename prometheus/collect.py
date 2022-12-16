# author: Yinqin Zhao

import datetime
import shutil
import sys, os
from prometheus_pandas import query
import time
from config import PROMETHEUS_URL, EXPORTERS, NODES, OUT_DIR


# CONFIGURE HERE

node_exporter_metrics = [
    "node_cpu_seconds_total_system",
    "node_cpu_seconds_total_user",
    "node_cpu_seconds_total_iowait",
    "node_cpu_seconds_total_idle",
    "node_network_receive_bytes_total",
    "node_network_transmit_bytes_total",
    "node_filesystem_used_bytes",
    "node_disk_read_bytes_total",
    "node_disk_written_bytes_total",
    "node_disk_read_time_seconds_total",
    "node_disk_write_time_seconds_total",
    "node_netstat_Tcp_CurrEstab",
    "node_sockstat_TCP_tw",
    "node_sockstat_sockets_used",
    "node_sockstat_UDP_inuse",
    "node_sockstat_TCP_alloc"
]
# Sequential mapped to node_exporter_metrics
def get_queries(ip):
    return [
        "avg(irate(node_cpu_seconds_total{instance=~\""+ip+":9100\",mode=\"system\"}[30m])) by (instance)",
        "avg(irate(node_cpu_seconds_total{instance=~\""+ip+":9100\",mode=\"user\"}[30m])) by (instance)",
        "avg(irate(node_cpu_seconds_total{instance=~\""+ip+":9100\",mode=\"iowait\"}[30m])) by (instance)",
        "avg(irate(node_cpu_seconds_total{instance=~\""+ip+":9100\",mode=\"idle\"}[30m])) by (instance)",
        "irate(node_network_receive_bytes_total{instance=~'"+ip+":9100',device!~'tap.*|veth.*|br.*|docker.*|virbr*|lo*'}[30m])*8",
        "irate(node_network_transmit_bytes_total{instance=~'"+ip+":9100',device!~'tap.*|veth.*|br.*|docker.*|virbr*|lo*'}[30m])*8",
        "1-(node_filesystem_free_bytes{instance=~'"+ip+":9100',fstype=~\"ext4|xfs\"} / node_filesystem_size_bytes{instance=~'"+ip+":9100',fstype=~\"ext4|xfs\"})",
        "irate(node_disk_read_bytes_total{instance=~\""+ip+":9100\"}[30m])",
        "irate(node_disk_written_bytes_total{instance=~\""+ip+":9100\"}[30m])",
        "irate(node_disk_read_time_seconds_total{instance=~\""+ip+":9100\"}[30m]) / irate(node_disk_reads_completed_total{instance=~\""+ip+":9100\"}[30m])",
        "irate(node_disk_write_time_seconds_total{instance=~\""+ip+":9100\"}[30m]) / irate(node_disk_writes_completed_total{instance=~\""+ip+":9100\"}[30m])",
        "node_netstat_Tcp_CurrEstab{instance=~'"+ip+":9100'}",
        "node_sockstat_TCP_tw{instance=~'"+ip+":9100'}",
        "node_sockstat_sockets_used{instance=~'"+ip+":9100'}",
        "node_sockstat_UDP_inuse{instance=~'"+ip+":9100'}",
        "node_sockstat_TCP_alloc{instance=~'"+ip+":9100'}"
    ]

start_time = "2022-12-12 9:00:00"
end_time = "2022-12-14 12:00:00"
steps = ["15s", "15s"] # or 1m 

# One query mapped to one dir
def gen_filedirlist():
    node_exporter_filedirlist = []
    for e in EXPORTERS:
        mkdir(OUT_DIR + e)
    for node in NODES:
        mkdir(OUT_DIR + "node-exporter/"+node["name"])
        for nem in node_exporter_metrics:
            mkdir(OUT_DIR + "node-exporter/"+node["name"]+"/"+nem)
            node_exporter_filedirlist.append(OUT_DIR +"node-exporter/"+node["name"]+"/"+nem)
    return node_exporter_filedirlist

def unix_time(dt):
  #转换成时间数组
  timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
  #转换成时间戳
  timestamp = time.mktime(timeArray)
  return timestamp


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径

start_datetimes_unix = [unix_time(start_time), unix_time(start_time)]
end_datetimes_unix = [unix_time(end_time), unix_time(end_time)]



def load_prometheus_data(output_folder,q):


    """ Loads data from a PromQL-compatible datasource

    :param output_folder: The path to the output folder

    """

    p = query.Prometheus(PROMETHEUS_URL)

    # Request the data from Prometheus instance
    counter = 0
    

    # split into hourly samples
    start_date = datetime.datetime.fromtimestamp(start_datetimes_unix[counter])
    end_date = datetime.datetime.fromtimestamp(end_datetimes_unix[counter])
    duration = end_date - start_date
    d_in_s = duration.total_seconds()
    hours_and_rest = divmod(d_in_s, 3600)
    hours = int(hours_and_rest[0])
    if hours_and_rest[1] != 0:
        hours += 1
    k = 0
    # Request the data from prometheus
    tf_start = start_date
    for i in range(hours):
        tf_end = tf_start + datetime.timedelta(hours=1)
        if tf_end > end_date:
            tf_end = end_date
        ts = p.query_range(query=q, start=tf_start, end=tf_end,
                            step=steps[counter])
        tf_start = tf_end
        file_name = output_folder + "/ts_" + str(k) + "_hour" + ".csv"
        #print(file_name,q)
        if ts.empty:
            continue
        ts.to_csv(file_name)
        k += 1
    counter += 1
    return


def to_zip_archive(output_folder):
    shutil.make_archive("output", 'zip', output_folder)


# Example Run: "python3 prometheus_2_csv.py output/"
if __name__ == "__main__":
    
    node_exporter_filedirlist = gen_filedirlist()
    #print(node_exporter_filedirlist)
    filedirindex = 0
    for node in NODES:
        ip = node["ip"]
        queries = get_queries(ip)
        #print(queries)
        for index in range(len(queries)):
            #print(node_exporter_filedirlist[filedirindex],queries[index])
            load_prometheus_data(node_exporter_filedirlist[filedirindex],queries[index])
            filedirindex += 1
