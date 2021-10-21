from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        return {'msg': 'Hello World POST'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
