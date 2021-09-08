#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

echo "Please run this script as superuser!"
read -p 'Username (which used to installed zookeeper before): ' USERNAME
echo ""

if [ -d "/home/$USERNAME" ]; then

  DEPENDENCIES="network.target remote-fs.target"
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
    echo "User=$USERNAME" >> $ZOOSERVICE
    echo "ExecStart=/home/$USERNAME/kafka/bin/zookeeper-server-start.sh /home/$USERNAME/kafka/config/zookeeper.properties" >> $ZOOSERVICE
    echo "ExecStop=/home/$USERNAME/kafka/bin/zookeeper-server-stop.sh" >> $ZOOSERVICE
    echo "Restart=on-abnormal" >> $ZOOSERVICE
    echo "" >> $ZOOSERVICE

    echo "[Install]" >> $ZOOSERVICE
    echo "WantedBy=multi-user.target" >> $ZOOSERVICE

    echo "$ZOOSERVICE created."

  fi

  ZOOKEEPERID=/data/zookeeper/myid
  if [ -f "$ZOOKEEPERID" ]; then
    echo "$ZOOKEEPERID found."
  else
    read -p 'Enter Zookeeper ID (number): ' ZKID
    echo ""
    mkdir /data
    cd /data
    mkdir zookeeper
    touch $ZOOKEEPERID
    echo $ZKID > $ZOOKEEPERID
  fi

else
  echo "There is no /home directory exists for user $USERNAME"
fi