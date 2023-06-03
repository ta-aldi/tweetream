from joblib import load
from config import TweetreamConsumer, TweetreamProducer, CONSUMER_CONF, PRODUCER_CONF, acked
import os, json
import pytz
from datetime import datetime


class Classifier():

    # load model
    def __init__(self, model_path, tf_idf_path, producer, consumer):
        self.model = load(model_path)
        self.tfidf = load(tf_idf_path)
        self.producer = producer
        self.consumer = consumer
        self.consumer.subscribe(['TWT-Cleaned'])

    # classify
    def run(self, raw_data):
        data = json.loads(raw_data)

        data['consumed_from_preprocessed_at'] = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        data['is_hate_speech'] = bool(self.model.predict(self.tfidf.transform([data.get('preprocessed_text', "")]))[0])
        data['injected_to_result_at'] = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f")

        str_data = json.dumps(data)
        self.producer.produce(data['tag'], str_data.encode('utf-8'), callback=acked)

    def listen(self):
        self.consumer.listen(self.run)


model_path = os.path.abspath('utils/model.joblib')
tf_idf_path = os.path.abspath('utils/tf_idf.joblib')
clf = Classifier(model_path, tf_idf_path, TweetreamProducer(PRODUCER_CONF), TweetreamConsumer(CONSUMER_CONF))
clf.listen()
# print(clf.run('jakarta lagi macet'))
# print(clf.run('jakarta ibu kota negara indonesia'))
