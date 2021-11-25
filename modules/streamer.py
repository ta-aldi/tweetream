from dotenv import load_dotenv
from preprocessor import Preprocessor
from config import acked
import os, tweepy, json

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Initialize Preprocessor Object
    def __init__(self, auth, preprocessor, producer, daemon=False):
        super(Stream, self).__init__(
            auth['TW_API_KEY'],
            auth['TW_API_KEY_SECRET'],
            auth['TW_ACCESS_TOKEN'],
            auth['TW_ACCESS_TOKEN_SECRET'],
            daemon=daemon
        )
        self.preprocessor = preprocessor
        self.producer = producer

    def filter_raw_data(self, raw_data):
        filtered = {}
        filtered['created_at'] = raw_data['created_at']
        filtered['text'] = raw_data['text']
        filtered['username'] = raw_data['user']['screen_name']
        return filtered

    # Process the text of any tweet that comes from the Twitter API
    def on_data(self, raw_data):
        data = raw_data.decode('utf-8')
        data = self.filter_raw_data(json.loads(data))
        data['text_cleaned'] = self.preprocessor.run(data['text'])
        data['tag'] = self.preprocessor.add_tag(data['text_cleaned'])
        data = json.dumps(data)
        self.producer.produce('TW-Cleaned', data.encode('utf-8'), callback=acked)
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
