from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
from streamer import Stream, auth, preprocessor, clf_path

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/topic')
def connect():
    topic = request.args.get('topic')
    print(topic)
    emit('message', 'hehe')

    # Create stream object with given credentials
    global stream
    stream = Stream(auth, preprocessor, clf_path, socketio)
    # Streaming filter
    stream_thread = stream.filter(
        track=[topic],
        threaded=True
    )

@socketio.on('disconnect', namespace='/topic')
def disconnect_cleanup():
    stream.disconnect()
    disconnect()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
