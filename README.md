# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## Kafka Installation Setup
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
bash scripts/start_service.sh
```

- Stop Kafka & Zookeeper Services
```
bash scripts/stop_service.sh
```