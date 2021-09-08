# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## [Development] Installation Setup
- Install Kafka
```
bash scripts/old_install_kafka.sh
```

- Configure Kafka & Zookeeper Properties
```
vi ~/kafka/config/server.properties
vi ~/kafka/config/zookeeper.properties
```

- Start Kafka & Zookeeper Services
```
bash scripts/old_start_kafka_service.sh
```

- Stop Kafka & Zookeeper Services
```
bash scripts/kafka/5_stop_kafka_service.sh
```

## [Production] Installation Setup
### Zookeeper Installation
- See scripts/zookeeper/zookeeper.txt for installation.

### Kafka Installation
- See scripts/kafka/kafka.txt for installation.
- For multi-node configuration, see example on scripts/server.properties
