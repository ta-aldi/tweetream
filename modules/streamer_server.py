from flask import Flask, request
from flask_cors import CORS, cross_origin
from streamer import Stream, auth, preprocessor
from config import TweetreamProducer, PRODUCER_CONF, create_topics

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            tags = request.json['tags']

            # close previously stream connection
            stream.disconnect()

            # register new tags
            preprocessor.register_tags(tags)

            # create new topic
            create_topics(tags)

            # recreate streamer
            setup_streamer()

            return {'msg': 'Success'}, 201
        except KeyError:
            return {'error': "The required field is 'tags' of type list of strings"}, 400

if __name__ == '__main__':
    setup_streamer()
    app.run(host='0.0.0.0', port=80)
