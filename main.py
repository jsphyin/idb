import logging

from flask import abort, render_template, request, jsonify
from sqlalchemy import column, literal, literal_column, text

import models

from extensions import app, db

def api(data):
    if not data:
        return jsonify([])
    return jsonify(data.json())

def paginated(query):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    instances = query.limit(per_page).offset((page - 1) * per_page).all()

    return jsonify({
        'page': page,
        'total_pages': -(-query.count() // per_page),
        'results': [i.json() for i in instances]
    })

def get_list(data):
    if data:
        return data.split('|')
    return []

def get_int_list(data):
    try:
        return [int(datum) for datum in data.split('|')]
    except ValueError:
        return []

@app.route('/api/games/<game_id>')
@app.route('/api/games/')
@app.route('/api/games')
def api_games(game_id=None):
    if game_id:
        return api(models.Game.query.get(game_id))

    q = models.Game.query

    genres = get_int_list(request.args.get('genres', ''))
    if genres:
        q = q.filter(models.Game.genres.any(models.Genre.id.in_(genres)))

    developers = get_int_list(request.args.get('developers', ''))
    if developers:
        q = q.filter(models.Game.developers.any(models.Developer.id.in_(developers)))

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

@app.route('/api/genres/<genre_id>')
@app.route('/api/genres/')
@app.route('/api/genres')
def api_genres(genre_id=None):
    if genre_id:
        return api(models.Genre.query.get(genre_id))

    q = models.Genre.query

    games = get_int_list(request.args.get('games', ''))
    if games:
        q = q.filter(models.Genre.games.any(models.Game.id.in_(games)))

    developers = get_int_list(request.args.get('developers', ''))
    if developers:
        q = q.filter(models.Genre.developers.any(models.Developer.id.in_(developers)))

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Genre.name)
    elif sort == '-name':
        q = q.order_by(models.Genre.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/developers/<developer_id>')
@app.route('/api/developers/')
@app.route('/api/developers')
def api_developers(developer_id=None):
    if developer_id:
        return api(models.Developer.query.get(developer_id))

    q = models.Developer.query

    games = get_int_list(request.args.get('games', ''))
    if games:
        q = q.filter(models.Developer.games.any(models.Game.id.in_(games)))

    genres = get_int_list(request.args.get('genres', ''))
    if genres:
        q = q.filter(models.Developer.genres.any(models.Genre.id.in_(genres)))

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Developer.name)
    elif sort == '-name':
        q = q.order_by(models.Developer.name.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/events/<event_id>')
@app.route('/api/events/')
@app.route('/api/events')
def api_events(event_id=None):
    if event_id:
        return api(models.Event.query.get(event_id))

    q = models.Event.query

    games = get_int_list(request.args.get('games', ''))
    if games:
        q = q.filter(models.Event.games.any(models.Game.id.in_(games)))

    genres = get_int_list(request.args.get('genres', ''))
    if genres:
        q = q.filter(models.Event.direct_genres.any(models.Genre.id.in_(genres)) |
                     models.Event.indirect_genres.any(models.Genre.id.in_(genres)))

    locations = get_list(request.args.get('locations', ''))
    if locations:
        q = q.filter(models.Event.location.in_(locations))

    sort = request.args.get('sort', 'name')
    if sort == 'name':
        q = q.order_by(models.Event.name)
    elif sort == '-name':
        q = q.order_by(models.Event.name.desc())
    elif sort == 'time':
        q = q.order_by(models.Event.time)
    elif sort == '-time':
        q = q.order_by(models.Event.time.desc())
    else:
        abort(400)

    return paginated(q)

@app.route('/api/games/names')
def api_games_names():
    return jsonify(models.Game.query.with_entities(models.Game.id, models.Game.primary_name).all())

@app.route('/api/genres/names')
def api_genres_names():
    return jsonify(models.Genre.query.with_entities(models.Genre.id, models.Genre.name).all())

@app.route('/api/developers/names')
def api_developers_names():
    return jsonify(models.Developer.query.with_entities(models.Developer.id, models.Developer.name).all())

@app.route('/api/events/names')
def api_events_names():
    return jsonify(models.Event.query.with_entities(models.Event.id, models.Event.name).all())

@app.route('/api/events/locations/names')
def api_events_locations():
    return jsonify([[loc[0],loc[0]] for loc in models.Event.query.with_entities(models.Event.location).distinct().all()])

@app.route('/api/search')
def api_search():
    query = request.args.get('query')
    if not query:
        abort(400)

    q = models.SearchResult.query.union_all(*(
        db.session.query(
            m.id.label(models.SearchResult.id.name),
            literal(m.__name__).label(models.SearchResult.type.name),
            literal_column(str(text(
                'MATCH ({}) AGAINST (:query IN NATURAL LANGUAGE MODE)'.format(m.__ftcolumns__)
                ).bindparams(query=query).compile(compile_kwargs={'literal_binds': True}))
            ).label(models.SearchResult.score.name)
        )
        for m in (models.Game, models.Genre, models.Developer, models.Event)
    )).order_by(models.SearchResult.score.desc())

    return paginated(q)

@app.route('/')
@app.route('/about')
@app.route('/search')
@app.route('/boardgame/<id>/<model>')
@app.route('/boardgamedesigner/<id>/<model>')
@app.route('/<any("game", "genre", "developer", "event"):model>/<id>')
@app.route('/<any("games", "genres", "developers", "events"):model>')
@app.route('/<any("games", "genres", "developers", "events"):model>/')
def grid(model=None, id=None):
    return render_template('index.html')

if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
