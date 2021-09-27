from dotenv import load_dotenv
import os, tweepy

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Prints the text of any tweet that comes from the Twitter API
    def on_status(self, status):
        print(status.text)

    # The Twitter API will send a 420 status code if we’re being rate limited -> disconnect
    def on_error(self, status_code):
        if status_code == 420:
            return False

    # On Disconnect event
    def on_disconnect(self):
        print("Connection Closed by Twitter")
        return False

stream = Stream(
    os.getenv('TW_API_KEY'),
    os.getenv('TW_API_KEY_SECRET'),
    os.getenv('TW_ACCESS_TOKEN'),
    os.getenv('TW_ACCESS_TOKEN_SECRET')
)

stream.filter(
    track=[
        "Mahasiswa"
    ]
)
