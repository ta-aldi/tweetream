# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## Apache Kafka Installation Setup
### [Development] Installation Setup
- Install Kafka
```
bash scripts/kafka/old_install_kafka.sh
```

- Configure Kafka & Zookeeper Properties
```
vi ~/kafka/config/server.properties
vi ~/kafka/config/zookeeper.properties
```

- Start Kafka & Zookeeper Services
```
bash scripts/kafka/old_start_kafka_service.sh
```

- Stop Kafka & Zookeeper Services
```
bash scripts/kafka/5_stop_kafka_service.sh
```

### [Production] Installation Setup
#### Zookeeper Installation
- See scripts/zookeeper/zookeeper.txt for installation.

#### Kafka Installation
- See scripts/kafka/kafka.txt for installation.
- For multi-node configuration, see example on scripts/server.properties

## Module Installation Setup (modules)
### Local Development
- Create virtual environment
```
# Windows
python -m venv env

# Mac/Linux
python3 -m venv env
```

- Activate virtual environment
```
# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

- Install dependencies
```
# Windows
pip install -r modules\requirements.txt

# Mac/Linux
pip3 install -r modules/requirements.txt
```

- Create environment file named **.env** by using **.env.sample** template.

- Run modules
```
# Windows
python modules\streamer_server.py
python modules\classifier.py

# Mac/Linux
python3 modules/streamer_server.py
python3 modules/classifier.py
```

- Deactivate virtual environment
```
deactivate
```

### Running as Background Services
- Create environment file named **.env** by using **.env.sample** template.

- Init .service files
```
bash scripts/node/1_init_preprocessor.sh
bash scripts/node/1_init_classifier.sh
```

- Start services
```
sudo systemctl start preprocessor
sudo systemctl start classifier
```

- Enable services on startup
```
sudo systemctl enable preprocessor
sudo systemctl enable classifier
```

## Web Server Installation (webclient)
- Go to webclient folder
```
cd webclient
```

- Install dependencies
```
go mod vendor
```

- Build & Run Project (Linux & Unix)
```
make go_run_web
```

- Build & Run Project (Windows or without **make** command)
```
go build -o bin/webclient main.go && go run main.go
```

- Or you want to run it as a Docker Container
```
bash start.sh
```

## Load Testing
- Create virtual environment
```
# Windows
python -m venv env

# Mac/Linux
python3 -m venv env
```

- Activate virtual environment
```
# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

- Install dependencies
```
# Windows
pip install -r tests\requirements.txt

# Mac/Linux
pip3 install -r tests/requirements.txt
```

- Go to **tests** directory
```
cd tests
```

- Run docker compose with n worker
```
docker-compose up --scale worker=n
```
