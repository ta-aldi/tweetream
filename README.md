# Tweetream
Cloud-based Real Time Tweet Streaming Platform for Large-Scale Microblogging Data Processing

## Author
Michael Susanto

## Background
As time goes by, more and more data are generated from activities carried out on the internet. To perform large-scale data processing, we need a way so that the data can be obtained and processed effectively and efficiently. One method for capturing large-scale data in real-time is by streaming them.

Research conducted by [Kurniawan et al.](https://ieeexplore.ieee.org/document/7863251) produce a best classification model that can be used for traffic classification. The application which is built by Kurniawan et al. can already perform streaming but its architecture is still using monolithic architecture and it is CLI-based program, which is not scalable when used to perform large-scale data processing. The term scalable here refers to the ability of the application to be scaled as needed and can be done on certain components of the application. Tweetream creates an architecture for doing real-time data processing by using classification model built by [Kurniawan et al.](https://ieeexplore.ieee.org/document/7863251) for testing its performance.

## About
Tweetream is a cloud-based real-time tweet streaming platform which aims to provide high availability and high performance with autoscaling configuration. Tweetream is able to accommodate the needs of large-scale data processing and it is scalable. The created architectural design for Tweetream is flexible enough so that inner components can be added and removed as needed. 

## Architecture 
In this project, there are five main components used to built Tweetream: Apache Zookeeper, Apache Kafka, Streamer, Classifier, and Web Client Application.

* **Apache Zookeeper** responsible for managing Apache Kafka clusters.
* **Apache Kafka** will act as the main distributed-system "data center" which provides loosely-coupled communication between nodes (Streamer, Classifier, Web Client Application) with publish-subscribe pattern. Apache Kafka also made nodes possible to get or publish data by streaming them.
* **Streamer** acts as a node to retrieve data from Twitter Streaming API and doing text preprocessing before sending them to Apache Kafka. Streamer also gives each preprocessed tweet a tag for classifier.
* **Classifier** acts as a node to retrieve preprocessed data from Streamer and doing text classification with model built by [Kurniawan et al.](https://ieeexplore.ieee.org/document/7863251) and send them back to Apache Kafka's topic based on the tag given by Streamer.
* **Web Client Application** acts as a node to serve end users. This node can be scaled using autoscaling configuration. End users can choose which topic they are interested to. These topics are filled by Classifier and ready to be consumed by end users. End users can also request new topics or delete some topics through this node, then this node will notify the Streamer to make changes. Note that Classifier is always synchronized with Streamer, so if the Streamer and Web Apps are synchronized, so does the Classifier.

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
