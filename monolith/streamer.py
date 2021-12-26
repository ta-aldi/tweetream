from dotenv import load_dotenv
from joblib import load
from preprocessor import Preprocessor
import os, tweepy, json

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Initialize Preprocessor Object
    def __init__(self, auth, preprocessor, model_path, daemon=False):
        super(Stream, self).__init__(
            auth['TW_API_KEY'],
            auth['TW_API_KEY_SECRET'],
            auth['TW_ACCESS_TOKEN'],
            auth['TW_ACCESS_TOKEN_SECRET'],
            daemon=daemon
        )
        self.preprocessor = preprocessor
        self.model = load(model_path)

    def filter_raw_data(self, raw_data):
        filtered = {}

        try:
            filtered['created_at'] = raw_data['created_at']
        except KeyError:
            filtered['created_at'] = 'No Date Specified'

        try:
            filtered['text'] = raw_data['text']
        except KeyError:
            filtered['text'] = 'No Tweet'

        try:
            filtered['username'] = raw_data['user']['screen_name']
        except:
            filtered['username'] = 'No Username (Anonymous)'
            
        return filtered

    # classify traffic/non-traffic tweets
    def classify(self, data):
        return self.model.predict([data['text_cleaned']])[0]

    # Process the text of any tweet that comes from the Twitter API
    def on_data(self, raw_data):
        data = raw_data.decode('utf-8')
        data = self.filter_raw_data(json.loads(data))
        data['text_cleaned'] = self.preprocessor.run(data['text'])
        data['prediction'] = self.classify(data)
        print(data)

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

# Create initial objects
preprocessor = Preprocessor()
clf_path = os.path.abspath('utils/LinSVCModel.joblib')

# # Create stream object with given credentials
# stream = Stream(auth, preprocessor, clf_path)
# # Streaming filter
# stream_thread = stream.filter(
#     track=["jakarta"]
# )
