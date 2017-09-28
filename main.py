import logging

from flask import Flask, render_template


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/games/catan')
def catan():
    return render_template('game_models/catan.html')

@app.route('/games/monopoly')
def monopoly():
    return render_template('game_models/monopoly.html')

@app.route('/games/clue')
def clue():
    return render_template('game_models/clue.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')

@app.route('/events')
def mechanics():
    return render_template('events.html')

if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
