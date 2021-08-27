#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# This script will create network tags called 'kafka' and 'zookeeper'
# 1. 'kafka', opens TCP port 9092
# 2. 'zookeeper', opens:
#     - TCP port 2181 (connecting client to zookeeper)
#     - TCP port 2888 (ZooKeeper peer connection)
#     - TCP port 3888 (leader election)

gcloud compute firewall-rules create kafka --allow=tcp:9092 --description="Allow incoming traffic on TCP port 9092" --direction=INGRESS
gcloud compute firewall-rules create zookeeper --allow=tcp:2181,tcp:2888,tcp:3888 --description="Allow incoming traffic on TCP port 2181,2888,3888" --direction=INGRESS
