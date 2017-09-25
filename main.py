import logging

from flask import Flask, render_template


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True)