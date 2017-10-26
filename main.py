import logging
import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

import json

from flask import Flask, render_template

with open('dummy.json') as data_file:
    data = json.load(data_file)

app = Flask(__name__, static_url_path='/static')

# for local: export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:boardgamers@127.0.0.1:3306/boardgamedb-data
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = bool(os.environ.get('SQLALCHEMY_ECHO', False))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api/games')
def games():
    print('Request received')
    return jsonify([1,2,3]);

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
