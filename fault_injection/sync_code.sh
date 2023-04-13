#!/bin/bash

cd ../devstack

DIR="../fault_injection"

vagrant scp $DIR/auto.py manager:~/auto.py
