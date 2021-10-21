from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
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
ADMIN_CONF = {'bootstrap.servers': BOOTSTRAP_SERVERS}

# Consumer & Producer Client
class TweetreamConsumer(Consumer):
    
    def __init__(self, config):
        super(TweetreamConsumer, self).__init__(config)

    def listen(self, processor):
        while True:
            msg = self.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            processor(msg.value().decode('utf-8'))


class TweetreamProducer(Producer):
    
    def __init__(self, config):
        super(TweetreamProducer, self).__init__(config)

consumer = TweetreamConsumer(CONSUMER_CONF)
producer = TweetreamProducer(PRODUCER_CONF)
admin = AdminClient(ADMIN_CONF)
excluded_topics = os.getenv('EXCLUDE_TOPICS').split(',')

# function to create new topic
def create_topics(topics):
    new_topics = [NewTopic(topic, num_partitions=2, replication_factor=2) for topic in topics]
    fs = admin.create_topics(new_topics)

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
