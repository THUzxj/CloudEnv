#!/bin/bash

source ../common.sh

set -x

USER_NAME="ubuntu"
REMOTE_PATH="/vagrant/configs/"
LOCAL_PATH="./configs/"

/usr/bin/env
rsync -r $USER_NAME@$K8S_MASTER_IP:$REMOTE_PATH $LOCAL_PATH
rsync -r $LOCAL_PATH $USER_NAME@$K8S_NODE01_IP:$REMOTE_PATH
