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

@app.route('/developers/teuber')
def teuber():
    return render_template('dev_models/teuber.html')

@app.route('/developers/magie')
def magie():
    return render_template('dev_models/magie.html')

@app.route('/developers/pratt')
def pratt():
    return render_template('dev_models/pratt.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')
    
@app.route('/genres/negotiation')
def negotiation():
    return render_template('genre_models/negotiation.html')
    
@app.route('/genres/economic')
def economic():
    return render_template('genre_models/economic.html')
    
@app.route('/genres/deduction')
def deduction():
    return render_template('genre_models/deduction.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/events/cwc')
def cwc():
    return render_template('event_models/cwc.html')

@app.route('/events/cec')
def cec():
    return render_template('event_models/cec.html')

@app.route('/events/mwc')
def mwc():
    return render_template('event_models/mwc.html')

if __name__ == '__main__':
    # Run locally in debug mode (gunicorn runs the app in production)
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
