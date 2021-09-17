# def hehe():
#     print("hehe")

# TEST = "test"
from confluent_kafka import Consumer, Producer
import socket

BOOTSTRAP_SERVERS = "x.x.x.x:9092,x.x.x.x:9092,x.x.x.x:9092"

CONSUMER_CONF = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': "foo",
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    'on_commit': commit_completed
}

PRODUCER_CONF = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'client.id': socket.gethostname()
}

consumer = Consumer(CONSUMER_CONF)
producer = Producer(PRODUCER_CONF)
