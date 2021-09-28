from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv
import socket, os

# Load dotenv library
load_dotenv()

# Callbacks
## Callback when consumer committed partition offsets
def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))

## Callback when producer produced messages
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# Configurations
BOOTSTRAP_SERVERS = os.getenv('KAFKA_SERVERS')
GROUP_ID = os.getenv('GROUP_ID')
CONSUMER_CONF = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}
PRODUCER_CONF = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'client.id': socket.gethostname()
}

# Consumer & Producer Client
consumer = Consumer(CONSUMER_CONF)
producer = Producer(PRODUCER_CONF)
