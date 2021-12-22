# Apache Kafka Cluster
These steps are required for each Virtual Machine instance in Kafka Cluster.

## Install Java OpenJDK
```
bash 1_install_java.sh
```

open ports for Kafka:
- TCP port 9092

## Create system user for kafka
```
sudo su
useradd kafka -m
usermod --shell /bin/bash kafka
passwd kafka
usermod -aG sudo kafka
exit
su - kafka
sudo cp -r ../<user>/kafka kafka
sudo chown -R kafka:kafka kafka
sudo chown -R kafka:kafka server.properties
```

## Download and install kafka
```
bash 2_download_kafka.sh
```

## Configure server.properties
See ```server.properties``` for sample configuration.

## Setup kafka config file
```
bash 3_setup_kafka_service.sh
```

## Start kafka service
```
bash 4_start_kafka_service.sh
```

## Stop kafka service
```
bash 5_stop_kafka_service.sh
```