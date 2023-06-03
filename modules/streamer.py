from dotenv import load_dotenv
from preprocessor import Preprocessor
from config import acked
import os, tweepy, json
import pytz
from datetime import datetime

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Initialize Preprocessor Object
    def __init__(self, auth, preprocessor, producer, daemon=False, **kwargs):
        super(Stream, self).__init__(
            auth['TW_API_KEY'],
            auth['TW_API_KEY_SECRET'],
            auth['TW_ACCESS_TOKEN'],
            auth['TW_ACCESS_TOKEN_SECRET'],
            daemon=daemon
        )
        self.preprocessor = preprocessor
        self.producer = producer
        self.consumer = kwargs.get("consumer")

    def _connect(self, method, endpoint, params=None, headers=None, body=None):
        self.running = True

        error_count = 0
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/connecting
        stall_timeout = 90
        network_error_wait = network_error_wait_step = 0.25
        network_error_wait_max = 16
        http_error_wait = http_error_wait_start = 5
        http_error_wait_max = 320
        http_420_error_wait_start = 60

        self.consumer.subscribe(['raw'])
        self.on_connect()

        try:
            while self.running and error_count <= self.max_retries:
                try:
                    msg = self.consumer.poll(1.0)

                    if msg is None:
                        error_count = 0
                        http_error_wait = http_error_wait_start
                        network_error_wait = network_error_wait_step

                        if not self.running:
                            break

                        continue

                    if msg.error():
                        self.on_connection_error(msg.error())
                        error_count += 1

                        if not self.running:
                            break

                        continue

                    error_count = 0
                    http_error_wait = http_error_wait_start
                    network_error_wait = network_error_wait_step

                    self.on_data(msg.value())

                except Exception as e:
                    self.on_connection_error()
                    if not self.running:
                        break

                    sleep(network_error_wait)

                    network_error_wait += network_error_wait_step
                    if network_error_wait > network_error_wait_max:
                        network_error_wait = network_error_wait_max

        except Exception as exc:
            self.on_exception(exc)

        finally:
            self.running = False
            self.on_disconnect()

    def filter_raw_data(self, raw_data):
        filtered = {
            "text": raw_data.get("text", "-No Text Found-"),
            "author": raw_data.get("author", "-No Author Found-"),
            "link": raw_data.get("link", "-No Link Found-"),
            "created_at": raw_data.get("created_at", "-No Created At Found-"),
            "injected_to_raw_at": raw_data.get("injected_to_raw_at", datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f")),
            "consumed_from_raw_at": datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f"),
        }

        return filtered

    # Process the text of any tweet that comes from the Twitter API
    def on_data(self, raw_data):
        data = raw_data.decode('utf-8')
        data = self.filter_raw_data(json.loads(data))

        data['preprocessed_text'] = self.preprocessor.run(data['text'])
        data['tag'] = self.preprocessor.add_tag(data['preprocessed_text'])
        data['injected_to_preprocessed_at'] = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        data = json.dumps(data)
        self.producer.produce('TWT-Cleaned', data.encode('utf-8'), callback=acked)
        self.producer.flush()

    # On Connect event
    def on_connect(self):
        print("Connected to Twitter Streaming API")

    # The Twitter API will send a 420 status code if we’re being rate limited -> disconnect
    def on_error(self, status_code):
        if status_code == 420:
            return False

    # On Disconnect event
    def on_disconnect(self):
        print("Connection Closed by Twitter")
        return False

# Auth Credentials
auth = {
    'TW_API_KEY': os.getenv('TW_API_KEY'),
    'TW_API_KEY_SECRET': os.getenv('TW_API_KEY_SECRET'),
    'TW_ACCESS_TOKEN': os.getenv('TW_ACCESS_TOKEN'),
    'TW_ACCESS_TOKEN_SECRET': os.getenv('TW_ACCESS_TOKEN_SECRET')
}

# Create preprocessor objects along and give initial keyword tags
preprocessor = Preprocessor()
# preprocessor.register_tags(['jakarta', 'macet'])
