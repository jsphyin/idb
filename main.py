import logging

from flask import abort, render_template, request, jsonify

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

    q = models.Game.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Game.primary_name)
    elif sort == '-name':
        q = q.order_by(models.Game.primary_name.desc())
    elif sort == 'year':
        q = q.order_by(models.Game.year)
    elif sort == '-year':
        q = q.order_by(models.Game.year.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/genres')
@app.route('/api/genres/<int:id>')
def api_genres(id=None):
    if id is not None:
        return jsonify(models.Genre.query.get(id).json())

    q = models.Genre.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Genre.name)
    elif sort == '-name':
        q = q.order_by(models.Genre.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/developers')
@app.route('/api/developers/<int:id>')
def api_developers(id=None):
    if id is not None:
        return jsonify(models.Developer.query.get(id).json())

    q = models.Developer.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Developer.name)
    elif sort == '-name':
        q = q.order_by(models.Developer.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/events')
@app.route('/api/events/<int:id>')
def api_events(id=None):
    if id is not None:
        return jsonify(models.Event.query.get(id).json())

    q = models.Event.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Event.name)
    elif sort == '-name':
        q = q.order_by(models.Event.name.desc())
    elif sort == 'location':
        q = q.order_by(models.Event.location)
    elif sort == '-location':
        q = q.order_by(models.Event.location.desc())
    elif sort == 'time':
        q = q.order_by(models.Event.time)
    elif sort == '-time':
        q = q.order_by(models.Event.time.desc())
    else:
        abort(400)

    return paginated(q)

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
