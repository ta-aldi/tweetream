from flask import Flask, request
from streamer import stream

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        return {'msg': 'Hello World POST'}

if __name__ == '__main__':
    # Streaming filter
    stream_thread = stream.filter(
        track=stream.preprocessor.tags,
        filter_level="low",
        threaded=True
    )
    app.run(host='0.0.0.0')
