#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Automating steps from: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-an-apache-zookeeper-cluster-on-ubuntu-18-04

# Please run this script as superuser!

# Installing java as one of Zookeeper dependencies
sudo apt update && sudo apt -y install default-jdk

# Create a data directory for Zookeeper
sudo mkdir -p /data/zookeeper

# Downloading and Extracting Zookeeper binaries
cd /opt
sudo curl https://dlcdn.apache.org/zookeeper/zookeeper-3.6.3/apache-zookeeper-3.6.3.tar.gz -o apache-zookeeper-3.6.3.tar.gz
sudo tar -xvf apache-zookeeper-3.6.3.tar.gz
sudo ln -s apache-zookeeper-3.6.3 zookeeper