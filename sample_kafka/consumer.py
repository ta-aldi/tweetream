from confluent_kafka import Consumer
from dotenv import load_dotenv
import os

# Load dotenv library
load_dotenv()

def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))

conf = {'bootstrap.servers': os.getenv('KAFKA_SERVERS'),
        'group.id': os.getenv('GROUP_ID'),
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'on_commit': commit_completed}

consumer = Consumer(conf)

# Client
running = True

def msg_process(msg):
    print('Received message: {}'.format(msg.value().decode('utf-8')))

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                print('No Message')
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

basic_consume_loop(consumer, [os.getenv('TOPICS_SUB')])