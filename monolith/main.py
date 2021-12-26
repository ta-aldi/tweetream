from flask import Flask, render_template
from config import admin

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    response = {
        "topics": admin.list_topics().topics
    }
    return render_template('index.html', **response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
