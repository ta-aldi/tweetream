from confluent_kafka import Producer
from dotenv import load_dotenv
import socket, os

# Load dotenv library
load_dotenv()

conf = {'bootstrap.servers': os.getenv('KAFKA_SERVERS'),
        'client.id': socket.gethostname()}

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

for i in range(10):
    producer.produce(os.getenv('TOPICS_PUB'), key="key", value="Hello Kafka", callback=acked)
    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    producer.poll(0)

producer.flush()