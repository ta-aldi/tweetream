#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Stopping and disable Kafka services
# Please run this script as superuser!
read -p 'Stop kafka service only (without Zookeeper)? [y/n]: ' KAFKAONLY
echo ""

if [ "$KAFKAONLY" = "n" ]; then
  sudo systemctl stop zookeeper
  sudo systemctl disable zookeeper
fi
sudo systemctl stop kafka
sudo systemctl disable kafka
