import logging

from flask import render_template, jsonify

import models

from extensions import app, db

@app.route('/api/<any("game", "genre", "developer", "event"):model>/<ID>')
def get_model(model, ID):
    model = models.map[model]
    instance = db.session.query(model).filter_by(id=ID).first()
    return jsonify(instance.json())

@app.route('/api/<any("games", "genres", "developers", "events"):model>/<page>')
@app.route('/api/<any("games", "genres", "developers", "events"):model>/')
def list_models(model, page=1):
    if model != 'events':
        model = models.map[model]
        instances = db.session.query(model).order_by(model.id).limit(99).offset(20 * (int(page) - 1))
    else:
        model = models.map[model]
        instances = db.session.query(model).order_by(model.id).limit(99).offset(300 + 20 * (int(page) - 1))
    return jsonify([instance.json() for instance in instances])

@app.route('/')
@app.route('/about')
@app.route('/<any("games", "genres", "developers", "events"):model>/<page>')
@app.route('/<any("games", "genres", "developers", "events"):model>/')
def grid(model, page=1):
    print('grid',model,page)
    return render_template('index.html')

@app.route('/<any("game", "genre", "developer", "event"):model>/<ID>')
def index(model, ID):
    print('instance',model,ID)
    return render_template('index.html')

"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
"""

if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)