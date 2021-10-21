from flask import Flask, request
from async_streamer import stream
import asyncio

app = Flask(__name__)

# async streaming task
stream_task = None
async def run_stream_task():
    # Streaming filter
    stream_task = stream.filter(
        track=stream.preprocessor.tags,
        filter_level="low"
    )
    await stream_task

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        print(stream_task)
        try:
            stream.preprocessor.register_tags(request.json['tags'])
            return {'msg': 'Success'}, 201
        except KeyError:
            return {'error': 'The required field is "tags" of type list of strings'}, 400

if __name__ == '__main__':
    asyncio.run(run_stream_task())
    app.run(host='0.0.0.0')
