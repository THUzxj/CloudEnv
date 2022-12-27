#!/bin/bash

cd ../devstack

DIR="../fault_injection"

/usr/bin/vagrant scp $DIR/auto.py manager:~/auto.py
mkdir -p $DIR/labels
/usr/bin/vagrant scp manager:~/fi*.log $DIR/labels
