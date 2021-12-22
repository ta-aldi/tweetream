# Apache Zookeeper Cluster
These steps are required for each Virtual Machine instance in Zookeeper Cluster.

## Source: https://www.howtoforge.com/how-to-install-apache-zookeeper-on-debian-10/

open ports for Zookeeper:
- TCP port 2181 (connecting client to zookeeper)
- TCP port 2888 (ZooKeeper peer connection)
- TCP port 3888 (leader election)

## Install Java OpenJDK
```
bash 1_install_java.sh
```

## Create system user for zookeeper
```
useradd zookeeper -m
usermod --shell /bin/bash zookeeper
passwd zookeeper
usermod -aG sudo zookeeper
su - zookeeper
```

## Download zookeeper
```
bash 2_download_zookeeper.sh
```

## Create zookeeper config file
```
bash 3_create_zookeeper_conf.sh
```

## Edit config file
```
sudo nano /opt/zookeeper/conf/zoo.cfg
```
See ```zoo.cfg``` for sample configuration.

## Return ownership to zookeeper
```
sudo chown -R zookeeper:zookeeper /opt/zookeeper
```

## Start zookeeper service
```
bash 4_start_zookeeper_service.sh
```

## Stop zookeeper service
```
bash 5_stop_zookeeper_service.sh
```