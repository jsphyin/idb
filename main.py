import logging

from flask import abort, render_template, request, jsonify
from sqlalchemy import column, literal, literal_column

import models

from extensions import app, db

def api(data):
    if not data:
        return jsonify([])
    return jsonify(data.json())

def paginated(query):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    instances = query \
        .limit(per_page) \
        .offset((page - 1) * per_page) \
        .all()

    return jsonify([i.json() for i in instances])

@app.route('/api/games/')
@app.route('/api/games')
def api_games():
    game_id = request.args.get('id', 0)
    if game_id:
        return jsonify(models.Game.query.get(game_id).json())

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

@app.route('/api/genres/')
@app.route('/api/genres')
def api_genres():
    genre_id = request.args.get('id', 0)
    if genre_id:
        return api(models.Genre.query.get(genre_id))

    q = models.Genre.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Genre.name)
    elif sort == '-name':
        q = q.order_by(models.Genre.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/developers/')
@app.route('/api/developers')
def api_developers():
    developer_id = request.args.get('id', 0)
    if developer_id:
        return api(models.Developer.query.get(developer_id))

    q = models.Developer.query

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Developer.name)
    elif sort == '-name':
        q = q.order_by(models.Developer.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/events/')
@app.route('/api/events')
def api_events():
    event_id = request.args.get('id', 0)
    if event_id:
        return api(models.Event.query.get(event_id))

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

@app.route('/api/search')
def api_search():
    query = request.args.get('query')
    if not query:
        abort(400)

    q = models.SearchResult.query.union_all(*(
        db.session.query(
            m.id.label(models.SearchResult.id.name),
            literal(m.__name__).label(models.SearchResult.type.name),
            literal_column('MATCH ({}) AGAINST (\'{}\' IN NATURAL LANGUAGE MODE)'.format(m.__ftcolumns__, query)).label(models.SearchResult.score.name)
        )
        for m in (models.Game, models.Genre, models.Developer, models.Event)
    )).order_by(models.SearchResult.score.desc())

    return paginated(q)

@app.route('/')
@app.route('/about')
@app.route('/<any("games", "genres", "developers", "events"):model>/')
@app.route('/<any("game", "genre", "developer", "event"):model>/')
@app.route('/<any("games", "genres", "developers", "events"):model>')
@app.route('/<any("game", "genre", "developer", "event"):model>')
def grid(model=None, params=None):
    return render_template('index.html')

if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
