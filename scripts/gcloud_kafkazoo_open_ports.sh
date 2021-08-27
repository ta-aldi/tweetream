#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Note: before running this Script, please create network tags first:
# You can create the required network tags for kafka & zookeeper with 
# `gcloud_kafkazoo_create_tags.sh` script

# This script attaches the instance with following network tags:
# 1. 'kafka', opens TCP port 9092
# 2. 'zookeeper', opens:
#     - TCP port 2181 (connecting client to zookeeper)
#     - TCP port 2888 (ZooKeeper peer connection)
#     - TCP port 3888 (leader election)

echo "This script requires existing network tags called: 'kafka' and 'zookeeper', which does the following actions:"
echo "'kafka' will opens TCP port 9092"
echo "'zookeeper' will opens:"
echo "  - TCP port 2181 (connecting client to zookeeper)"
echo "  - TCP port 2888 (ZooKeeper peer connection)"
echo "  - TCP port 3888 (leader election)"
echo ""
read -p 'Enter instance name: ' INSTANCENAME
gcloud compute instances add-tags $INSTANCENAME --zone us-central1-a --tags kafka,zookeeper
echo "Network tags 'kafka' and 'zookeeper' added into instance with name $INSTANCENAME"
