#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Automating steps from: https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-debian-10

echo "Please run this script as superuser!"
read -p 'Generate kafka service only (without Zookeeper)? [y/n]: ' KAFKAONLY
echo ""

DEPENDENCIES="network.target remote-fs.target"

if [ "$KAFKAONLY" = "n" ]; then
  # check if zookeeper.service file is already created, the service file will be created if not.
  # ZOOSERVICE=/etc/systemd/system/zookeeper.service
  ZOOSERVICE=/etc/systemd/system/zookeeper.service
  if [ -f "$ZOOSERVICE" ]; then
    echo "$ZOOSERVICE found."
  else
    touch $ZOOSERVICE

    echo "[Unit]" >> $ZOOSERVICE
    echo "Requires=$DEPENDENCIES" >> $ZOOSERVICE
    echo "After=$DEPENDENCIES" >> $ZOOSERVICE
    echo "" >> $ZOOSERVICE

    echo "[Service]" >> $ZOOSERVICE
    echo "Type=simple" >> $ZOOSERVICE
    echo "User=kafka" >> $ZOOSERVICE
    echo "ExecStart=/home/kafka/bin/zookeeper-server-start.sh /home/kafka/config/zookeeper.properties" >> $ZOOSERVICE
    echo "ExecStop=/home/kafka/bin/zookeeper-server-stop.sh" >> $ZOOSERVICE
    echo "Restart=on-abnormal" >> $ZOOSERVICE
    echo "" >> $ZOOSERVICE

    echo "[Install]" >> $ZOOSERVICE
    echo "WantedBy=multi-user.target" >> $ZOOSERVICE

    echo "$ZOOSERVICE created."

  fi

  DEPENDENCIES="zookeeper.service"

  sudo systemctl start zookeeper
  sudo systemctl enable zookeeper

fi  

# check if kafka.service file is already created, the service file will be created if not.
# KAFKASERVICE=/etc/systemd/system/kafka.service
KAFKASERVICE=/etc/systemd/system/kafka.service
if [ -f "$KAFKASERVICE" ]; then
  echo "$KAFKASERVICE found."
else
  touch $KAFKASERVICE

  echo "[Unit]" >> $KAFKASERVICE
  echo "Requires=$DEPENDENCIES" >> $KAFKASERVICE
  echo "After=$DEPENDENCIES" >> $KAFKASERVICE
  echo "" >> $KAFKASERVICE

  echo "[Service]" >> $KAFKASERVICE
  echo "Type=simple" >> $KAFKASERVICE
  echo "User=kafka" >> $KAFKASERVICE
  echo "ExecStart=/bin/sh -c '/home/kafka/bin/kafka-server-start.sh /home/kafka/config/server.properties > /home/kafka/kafka.log 2>&1'" >> $KAFKASERVICE
  echo "ExecStop=/home/kafka/bin/kafka-server-stop.sh" >> $KAFKASERVICE
  echo "Restart=on-abnormal" >> $KAFKASERVICE
  echo "" >> $KAFKASERVICE

  echo "[Install]" >> $KAFKASERVICE
  echo "WantedBy=multi-user.target" >> $KAFKASERVICE

  echo "$KAFKASERVICE created."
fi