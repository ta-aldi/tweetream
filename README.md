# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## [Development] Installation Setup
- Install Kafka
```
bash scripts/install_kafka.sh
```

- Configure Kafka & Zookeeper Properties
```
vi ~/kafka/config/server.properties
vi ~/kafka/config/zookeeper.properties
```

- Start Kafka & Zookeeper Services
```
bash scripts/start_kafka_service.sh
```

- Stop Kafka & Zookeeper Services
```
bash scripts/stop_kafka_service.sh
```

## [Production] Installation Setup
### Zookeeper Installation
- See scripts/zookeeper/zookeeper.txt for installation.

### Kafka Installation
- Install Kafka
```
bash scripts/install_kafka.sh
```

- Configure Kafka Properties
```
vi ~/kafka/config/server.properties
```

- Start Kafka Services
```
bash scripts/start_kafka_service.sh
```

- Stop Kafka Services
```
bash scripts/stop_kafka_service.sh
```
