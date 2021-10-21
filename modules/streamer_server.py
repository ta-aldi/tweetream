from flask import Flask, request
from streamer import Stream, auth, preprocessor
from config import TweetreamProducer, PRODUCER_CONF

app = Flask(__name__)

def setup_streamer():
    global stream

    # Create stream object with given credentials
    stream = Stream(auth, preprocessor, TweetreamProducer(PRODUCER_CONF))
    # Streaming filter
    stream_thread = stream.filter(
        track=stream.preprocessor.tags,
        filter_level="low",
        threaded=True
    )

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            tags = request.json['tags']

            # close previously stream connection
            stream.disconnect()

            # register new tags
            preprocessor.register_tags(tags)

            # recreate streamer
            setup_streamer()

            return {'msg': 'Success'}, 201
        except KeyError:
            return {'error': "The required field is 'tags' of type list of strings"}, 400

if __name__ == '__main__':
    setup_streamer()
    app.run(host='0.0.0.0')
