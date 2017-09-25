import logging

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'IDB - SWE Project'


if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True)