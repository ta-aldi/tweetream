#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Automating steps from: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-an-apache-zookeeper-cluster-on-ubuntu-18-04

# Please run this script as superuser!

echo "Please run this script as superuser!"

ZOOCFG=/opt/zookeeper/conf/zoo.cfg
if [ -f "$ZOOCFG" ]; then
  echo "$ZOOCFG found."
else
  touch $ZOOCFG

  echo "tickTime=2000" >> $ZOOCFG
  echo "dataDir=/data/zookeeper" >> $ZOOCFG
  echo "clientPort=2181" >> $ZOOCFG
  echo "maxClientCnxns=60" >> $ZOOCFG
  echo "initLimit=10" >> $ZOOCFG
  echo "syncLimit=5" >> $ZOOCFG
  echo "server.1=<host>:2888:3888" >> $ZOOCFG
  echo "server.2=<host>:2888:3888" >> $ZOOCFG
  echo "server.3=<host>:2888:3888" >> $ZOOCFG

  sudo chown -R zookeeper:zookeeper /opt/zookeeper
fi

ZOOSERVICE=/etc/systemd/system/zookeeper.service
if [ -f $ZOOSERVICE ]; then
  echo "$ZOOSERVICE found."
else
  touch $ZOOSERVICE

  echo "[Unit]" >> $ZOOSERVICE
  echo "Description=Zookeeper Daemon" >> $ZOOSERVICE
  echo "Documentation=http://zookeeper.apache.org" >> $ZOOSERVICE
  echo "Requires=network.target" >> $ZOOSERVICE
  echo "After=network.target" >> $ZOOSERVICE
  echo "" >> $ZOOSERVICE

  echo "[Service]" >> $ZOOSERVICE
  echo "Type=forking" >> $ZOOSERVICE
  echo "WorkingDirectory=/opt/zookeeper" >> $ZOOSERVICE
  echo "User=zookeeper" >> $ZOOSERVICE
  echo "Group=zookeeper" >> $ZOOSERVICE
  echo "ExecStart=/opt/zookeeper/bin/zkServer.sh start /opt/zookeeper/conf/zoo.cfg" >> $ZOOSERVICE
  echo "ExecStop=/opt/zookeeper/bin/zkServer.sh stop /opt/zookeeper/conf/zoo.cfg" >> $ZOOSERVICE
  echo "ExecReload=/opt/zookeeper/bin/zkServer.sh restart /opt/zookeeper/conf/zoo.cfg" >> $ZOOSERVICE
  echo "TimeoutSec=30" >> $ZOOSERVICE
  echo "Restart=on-failure" >> $ZOOSERVICE
  echo "" >> $ZOOSERVICE

  echo "[Install]" >> $ZOOSERVICE
  echo "WantedBy=default.target" >> $ZOOSERVICE

  echo "$ZOOSERVICE created."
fi

ZOOKEEPERID=/data/zookeeper/myid
if [ -f "$ZOOKEEPERID" ]; then
  echo "$ZOOKEEPERID found."
else
  read -p 'Enter Zookeeper ID (number): ' ZKID
  echo ""
  touch $ZOOKEEPERID
  echo $ZKID > $ZOOKEEPERID

  sudo chown -R zookeeper:zookeeper /data/zookeeper
fi
