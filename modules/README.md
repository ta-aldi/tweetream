# Tweetream (Modules)
This folder contains all independent modules / services that can be pipelined with Apache Kafka.

## Author
Michael Susanto

## Modules
There are three main modules used in this platform:

### Streamer
This module ingests data from data source of Twitter Streaming API and preprocesses them (by doing text preprocessing and cleaning the text) before they are being sent to Apache Kafka.

Related files:
- streamer_server.py
    - Contains Flask Web Server to serve HTTP Requests for adding or removing topics.
    - The streamer will be run on separate thread.
- streamer.py
    - Main file for getting real-time Tweet data through Twitter Streaming API with Tweepy.
    - This module run on separate thread, responsible for streaming and publishing data to Apache Kafka topics.
- preprocessor.py
    - This file does the text preprocessing over the coming tweets from streamer.py, before they're being sent to Apache Kafka by streamer.py.

How to run: see folder ```scripts/node/README.md```

### Classifier
This module consumes preprocessed tweets from Streamer and doing traffic classification based on model built by [Kurniawan et al.](https://ieeexplore.ieee.org/document/7863251).

Related files:
- classifier.py
    - Provide your model into ```utils/model.joblib``` or anything and change the ```clf_path``` in this file.

How to run: see folder ```scripts/node/README.md```

### Web Client
See ```webclient``` folder outside of this module.