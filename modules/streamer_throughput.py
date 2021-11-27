from dotenv import load_dotenv
import os, tweepy, time, multiprocessing

# Load dotenv library
load_dotenv()

# User-defined Tweepy Stream listener class
class Stream(tweepy.Stream):

    # Initialize Preprocessor Object
    def __init__(self, auth, total_timer=3600, interval=300, daemon=False):
        super(Stream, self).__init__(
            auth['TW_API_KEY'],
            auth['TW_API_KEY_SECRET'],
            auth['TW_ACCESS_TOKEN'],
            auth['TW_ACCESS_TOKEN_SECRET'],
            daemon=daemon
        )
        self.total_timer = total_timer
        self.interval = interval
        self.tweet_count = multiprocessing.Value('i', 0)
        self.tweet_counts_arr = multiprocessing.Array('i', [0]*(self.total_timer // self.interval))
        self.timer_process = multiprocessing.Process(target=self.countup, args=(self.total_timer, self.interval))

    # Process the text of any tweet that comes from the Twitter API
    def on_data(self, raw_data):
        data = raw_data.decode('utf-8')
        self.tweet_count.value += 1

    # On Connect event
    def on_connect(self):
        print("Connected to Twitter Streaming API")
        self.timer_process.start()

    # The Twitter API will send a 420 status code if we’re being rate limited -> disconnect
    def on_error(self, status_code):
        if status_code == 420:
            return False

    # On Disconnect event
    def on_disconnect(self):
        print("Connection Closed by Twitter")
        return False
    
    # function to count up per second until specified time (in seconds)
    def countup(self, sec, interval):
        current = 1
        print(self.tweet_counts_arr[:])
        print("=====================")
        while current <= sec:
            if current % interval == 0:
                self.tweet_counts_arr[(current // interval)-1] = self.tweet_count.value
                print(self.tweet_counts_arr[:])
                self.tweet_count.value = 0

            # print(current)
            time.sleep(1)
            current += 1
        print("=====================")
        print(self.tweet_counts_arr[:])

# Auth Credentials
auth = {
    'TW_API_KEY': os.getenv('TW_API_KEY'),
    'TW_API_KEY_SECRET': os.getenv('TW_API_KEY_SECRET'),
    'TW_ACCESS_TOKEN': os.getenv('TW_ACCESS_TOKEN'),
    'TW_ACCESS_TOKEN_SECRET': os.getenv('TW_ACCESS_TOKEN_SECRET')
}

if __name__=='__main__':
    # Create stream object with given credentials
    stream = Stream(auth)
    # Streaming filter
    stream_thread = stream.filter(
        track=['tag'],
    )
