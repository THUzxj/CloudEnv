#!/bin/bash
#
# Setup for Node servers

set -euxo pipefail

config_path="/vagrant/configs"
user="ubuntu"

/bin/bash $config_path/join.sh -v

sudo -i -u ubuntu bash << EOF
whoami
mkdir -p /home/$user/.kube
sudo cp -i $config_path/config /home/$user/.kube/
sudo chown 1000:1000 /home/$user/.kube/config
NODENAME=$(hostname -s)
kubectl label node $(hostname -s) node-role.kubernetes.io/worker=worker
EOF
