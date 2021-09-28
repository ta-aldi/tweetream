from joblib import load
from config import TweetreamConsumer, TweetreamProducer, CONSUMER_CONF, PRODUCER_CONF, acked
import os

class Classifier():

    # load model
    def __init__(self, model_path, producer, consumer):
        self.model = load(model_path)
        self.producer = producer
        self.consumer = consumer
        self.consumer.subscribe(['TWCleaned'])

    # classify
    def run(self, text):
        prediction = self.model.predict([text])[0]
        self.producer.produce('TWClassified', prediction.encode('utf-8'), callback=acked)

    def listen(self):
        self.consumer.listen(self.run)


clf_path = os.path.abspath('utils/LinSVCModel.joblib')
clf = Classifier(clf_path, TweetreamProducer(PRODUCER_CONF), TweetreamConsumer(CONSUMER_CONF))
clf.listen()
# print(clf.run('jakarta lagi macet'))
# print(clf.run('jakarta ibu kota negara indonesia'))
