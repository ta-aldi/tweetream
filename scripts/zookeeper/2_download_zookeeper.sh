#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Downloading and Extracting Zookeeper binaries
cd /opt
sudo curl https://dlcdn.apache.org/zookeeper/zookeeper-3.6.3/apache-zookeeper-3.6.3-bin.tar.gz -o apache-zookeeper-3.6.3-bin.tar.gz
sudo tar -xzvf apache-zookeeper-3.6.3-bin.tar.gz
sudo mv apache-zookeeper-3.6.3-bin zookeeper
sudo chown -R zookeeper:zookeeper /opt/zookeeper

# Create data directory
sudo mkdir -p /data/zookeeper
sudo chown -R zookeeper:zookeeper /data/zookeeper