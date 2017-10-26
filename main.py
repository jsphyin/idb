import logging
import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

import json

from flask import Flask, render_template
import models

app = Flask(__name__, static_url_path='/static')

# for local: export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:boardgamers@127.0.0.1:3306/boardgamedb-data
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = bool(os.environ.get('SQLALCHEMY_ECHO', False))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api/<any("game", "genre", "developer", "event"):model>/<ID>')
def get_model(model, ID):
    model = models.map[model]
    instance = db.session.query(model).filter_by(id=ID).first()
    return jsonify(instance.json())

@app.route('/api/<any("games", "genres", "developers", "events"):model>/<page>')
@app.route('/api/<any("games", "genres", "developers", "events"):model>/')
def list_models(model, page=1):
    model = models.map[model]
    instances = db.session.query(model).order_by(model.id).limit(20).offset(20 * (page - 1))
    return jsonify([instance.json() for instance in instances])

@app.route('/')
@app.route('/games')
@app.route('/genres')
@app.route('/developers')
@app.route('/events')
@app.route('/about')
def grid():
    return render_template('index.html')

@app.route('/game/<ID>')
@app.route('/genre/<ID>')
@app.route('/developer/<ID>')
@app.route('/event/<ID>')
def index(ID):
    return render_template('index.html')

"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
"""

if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
