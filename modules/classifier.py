from joblib import load
from config import TweetreamConsumer, TweetreamProducer, CONSUMER_CONF, PRODUCER_CONF, acked
import os, json

class Classifier():

    # load model
    def __init__(self, model_path, producer, consumer):
        self.model = load(model_path)
        self.producer = producer
        self.consumer = consumer
        self.consumer.subscribe(['TWCleaned'])

    # classify
    def run(self, raw_data):
        data = json.loads(raw_data)
        data['prediction'] = self.model.predict([data['text_cleaned']])[0]
        data = json.dumps(data)
        self.producer.produce('TWClassified', data.encode('utf-8'), callback=acked)

    def listen(self):
        self.consumer.listen(self.run)


clf_path = os.path.abspath('utils/LinSVCModel.joblib')
clf = Classifier(clf_path, TweetreamProducer(PRODUCER_CONF), TweetreamConsumer(CONSUMER_CONF))
clf.listen()
# print(clf.run('jakarta lagi macet'))
# print(clf.run('jakarta ibu kota negara indonesia'))
