#!/bin/bash

cd ../devstack

DIR="../data_v2/origin_data/fi_logs"

mkdir -p $DIR
vagrant scp manager:~/fi*.log $DIR
