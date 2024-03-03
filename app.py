from flask import Flask, render_template, Response

from consumer import start_consuming

app = Flask(__name__)


@app.route('/topic/<topic_name>')
def get_messages(topic_name):
    return Response(start_consuming([topic_name]), mimetype='text/event-stream')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
