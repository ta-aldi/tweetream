# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## Kafka Installation Setup
- Install Kafka
```
scripts/install_kafka.sh
```

- Configure Kafka & Zookeeper Properties
```
vi ~/kafka/config/server.properties
vi ~/kafka/config/zookeeper.properties
```

- Start Kafka & Zookeeper Services
```
scripts/start_service.sh
```