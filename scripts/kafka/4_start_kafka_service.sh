#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Starting and enabling services
# Please run this script as superuser!
read -p 'Start kafka service only (without Zookeeper)? [y/n]: ' KAFKAONLY
echo ""

if [ "$KAFKAONLY" = "n" ]; then
  sudo systemctl start zookeeper
  sudo systemctl enable zookeeper
fi
sudo systemctl start kafka
sudo systemctl enable kafka
