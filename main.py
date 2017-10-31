import logging

from flask import render_template, request, jsonify

import models

from extensions import app, db


def paginated(query):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    instances = query \
        .order_by('id') \
        .limit(per_page) \
        .offset((page - 1) * per_page) \
        .all()

    return jsonify([i.json() for i in instances])

@app.route('/api/games')
@app.route('/api/games/<int:id>')
def api_games(id=None):
    if id is not None:
        return jsonify(models.Game.query.get(id).json())

    return paginated(models.Game.query)

@app.route('/api/genres')
@app.route('/api/genres/<int:id>')
def api_genres(id=None):
    if id is not None:
        return jsonify(models.Genre.query.get(id).json())

    return paginated(models.Genre.query)

@app.route('/api/developers')
@app.route('/api/developers/<int:id>')
def api_developers(id=None):
    if id is not None:
        return jsonify(models.Developer.query.get(id).json())

    return paginated(models.Developer.query)

@app.route('/api/events')
@app.route('/api/events/<int:id>')
def api_events(id=None):
    if id is not None:
        return jsonify(models.Event.query.get(id).json())

    return paginated(models.Event.query)

@app.route('/')
@app.route('/about')
@app.route('/<any("games", "genres", "developers", "events"):model>/<page>')
@app.route('/<any("games", "genres", "developers", "events"):model>/')
def grid(model=None, page=1):
    return render_template('index.html')

@app.route('/<any("game", "genre", "developer", "event"):model>/<ID>')
def index(model, ID):
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
