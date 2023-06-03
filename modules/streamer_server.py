from flask import Flask, request
from flask_cors import CORS, cross_origin
from streamer import Stream, auth, preprocessor
from config import TweetreamProducer, TweetreamConsumer, PRODUCER_CONF, CONSUMER_CONF, create_topics, delete_topics

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def setup_streamer():
    global stream

    consumer_config = {
        **CONSUMER_CONF,
        'group.id': "mock-twitter-streamer",
    }
    stream = Stream(auth, preprocessor, TweetreamProducer(PRODUCER_CONF), consumer=TweetreamConsumer(consumer_config))
    # Streaming filter
    stream_thread = stream.filter(
        track=stream.preprocessor.tags,
        filter_level="low",
        threaded=True
    )

@app.route('/', methods=['POST', 'DELETE'])
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
        except:
            return {'error': "Unknown Error Occured, failed to create topic"}, 500

    elif request.method == 'DELETE':
        try:
            tags = request.json['tags']

            # close previously stream connection
            stream.disconnect()

            # unregister tags
            preprocessor.unregister_tags(tags)

            # delete topic
            delete_topics(tags)

            # recreate streamer
            setup_streamer()

            return {'msg': 'Success'}, 201
        except KeyError:
            return {'error': "The required field is 'tags' of type list of strings"}, 400
        except:
            return {'error': "Unknown Error Occured, failed to delete topic"}, 500

if __name__ == '__main__':
    setup_streamer()
    app.run(host='0.0.0.0', port=5000)
