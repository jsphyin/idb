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

@app.route('/games/<game>')
def gameInstance(game):
    return render_template('game_models/'+game+'.html')


@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/developers/<developer>')
def devInstance(developer):
    return render_template('dev_models/'+developer+'.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')
    
@app.route('/genres/<genre>')
def genreInstance(genre):
    return render_template('genre_models/'+genre+'.html')


@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/events/<event>')
def eventInstance(event):
    return render_template('event_models/'+event+'.html')

if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
