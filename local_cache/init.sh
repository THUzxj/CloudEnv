#!/bin/sh

HOST_IP=192.168.121.1

echo "Acquire::http::proxy \"http://$HOST_IP\";" > /etc/apt/apt.conf.d/00aptproxy

sed -i 's/http:\/\/.*.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/' /etc/apt/sources.list

pip3 config set global.index-url https://$HOST_IP:8005/root/pypi/+simple
