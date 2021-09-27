from dotenv import load_dotenv
from preprocessor import Preprocessor
import os, tweepy

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Initialize Preprocessor Object
    def __init__(self, auth, preprocessor):
        super(Stream, self).__init__(
            auth['TW_API_KEY'],
            auth['TW_API_KEY_SECRET'],
            auth['TW_ACCESS_TOKEN'],
            auth['TW_ACCESS_TOKEN_SECRET']
        )
        self.preprocessor = preprocessor

    # Process the text of any tweet that comes from the Twitter API
    def on_status(self, status):
        preprocessed = self.preprocessor.run(status.text)
        print(preprocessed)

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

# Create stream object with given credentials
stream = Stream(auth, Preprocessor())

# Streaming filter
stream.filter(
    track=[
        "Mahasiswa"
    ]
)
