from config import TweetreamConsumer, CONSUMER_CONF

c = TweetreamConsumer(CONSUMER_CONF)

c.subscribe(['TWClassified'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()