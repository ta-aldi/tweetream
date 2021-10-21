from flask import Flask, request
from streamer import stream

app = Flask(__name__)
stream_thread = None

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        print(stream_thread)
        try:
            stream.preprocessor.register_tags(request.json['tags'])
            return {'msg': 'Success'}, 201
        except KeyError:
            return {'error': 'The required field is "tags" of type list of strings'}, 400

if __name__ == '__main__':
    # Streaming filter
    stream_thread = stream.filter(
        track=stream.preprocessor.tags,
        filter_level="low",
        threaded=True
    )
    app.run(host='0.0.0.0')
