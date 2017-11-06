from extensions import db

from sqlalchemy.ext.hybrid import hybrid_property

game_family_assoc = db.Table('game_family_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('family_id', db.Integer, db.ForeignKey('family.id'), primary_key=True)
)

game_genre_assoc = db.Table('game_genre_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

game_publisher_assoc = db.Table('game_publisher_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True)
)

game_artist_assoc = db.Table('game_artist_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)

game_developer_assoc = db.Table('game_developer_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('developer_id', db.Integer, db.ForeignKey('developer.id'), primary_key=True)
)

game_mechanic_assoc = db.Table('game_mechanic_assoc',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id'), primary_key=True)
)

event_game_assoc = db.Table('event_game_assoc',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

event_genre_assoc = db.Table('event_genre_assoc',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), primary_key=True)
    score = db.Column(db.Float, primary_key=True)

    def json(self):
        return {'id': self.id,
            'type': self.type,
            'score': self.score
            }

class Game(db.Model):
    __ftcolumns__ = 'primary_name, alt_names, raw_desc'

    id = db.Column(db.Integer, primary_key=True)

    is_expansion = db.Column(db.Boolean)

    primary_name = db.Column(db.String(4096))
    alt_names = db.Column(db.Text)

    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)
    raw_desc = db.Column(db.Text)

    year = db.Column(db.Integer)

    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)

    rating = db.Column(db.Float)

    families = db.relationship('Family', secondary=game_family_assoc, back_populates='games')
    genres = db.relationship('Genre', secondary=game_genre_assoc, back_populates='games')
    publishers = db.relationship('Publisher', secondary=game_publisher_assoc, back_populates='games')
    artists = db.relationship('Artist', secondary=game_artist_assoc, back_populates='games')
    developers = db.relationship('Developer', secondary=game_developer_assoc, back_populates='games')
    mechanics = db.relationship('Mechanic', secondary=game_mechanic_assoc, back_populates='games')
    events = db.relationship('Event', secondary=event_game_assoc, back_populates='games')

    def json(self):
        return {'id': self.id,
            'is_expansion': self.is_expansion,
            'name': self.primary_name,
            'alt_names': self.alt_names.split(',') if self.alt_names else [],
            'img': self.image,
            'desc': self.desc,
            'families': [(family.id, family.name) for family in self.families],
            'genres': [(genre.id, genre.name) for genre in self.genres],
            'year': self.year,
            'publishers': [(publisher.id, publisher.name) for publisher in self.publishers],
            'artists': [(artist.id, artist.name) for artist in self.artists],
            'developers': [(developer.id, developer.name) for developer in self.developers],
            'mechanics': [(mechanic.id, mechanic.name) for mechanic in self.mechanics],
            'min_players': self.min_players,
            'max_players': self.max_players,
            'rating': self.rating
            }

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_family_assoc, back_populates='families')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.primary_name) for game in self.games]
                }

class Genre(db.Model):
    __ftcolumns__ = 'name, raw_desc'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)
    raw_desc = db.Column(db.Text)

    games = db.relationship('Game', secondary=game_genre_assoc, back_populates='genres')
    direct_events = db.relationship('Event', secondary=event_genre_assoc, back_populates='genres')

    def json(self):
        return {'id': self.id,
                'img': self.image,
                'name': self.name,
                'desc': self.desc,
                'games': [(game.id, game.primary_name) for game in self.games],
                'events': [(event.id, event.name) for event in self.events],
                'developers': [(developer.id, developer.name) for developer in self.developers]
                }

    @hybrid_property
    def developers(self):
        return Developer.query \
            .join(Developer.games) \
            .join(Game.genres) \
            .filter(Genre.id == self.id) \
            .all()

    @hybrid_property
    def events(self):
        if self.direct_events:
            return self.direct_events

        return Event.query \
            .join(Event.games) \
            .join(Game.genres) \
            .filter(Genre.id == self.id) \
            .all()

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_publisher_assoc, back_populates='publishers')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.primary_name) for game in self.games]
                }

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_artist_assoc, back_populates='artists')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.primary_name) for game in self.games]
                }

class Developer(db.Model):
    __ftcolumns__ = 'name, raw_desc, website'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)
    raw_desc = db.Column(db.Text)
    website = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_developer_assoc, back_populates='developers')

    def json(self):
        return {'id': self.id,
                'img': self.image,
                'name': self.name,
                'desc': self.desc,
                'games': [(game.id, game.primary_name) for game in self.games],
                'genres': [(genre.id, genre.name) for genre in self.genres],
                'website': self.website
                }

    @hybrid_property
    def genres(self):
        return Genre.query \
            .join(Genre.games) \
            .join(Game.developers) \
            .filter(Developer.id == self.id) \
            .all()

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_mechanic_assoc, back_populates='mechanics')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.primary_name) for game in self.games]
                }

class Event(db.Model):
    __ftcolumns__ = 'name, raw_desc, location, link'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    desc = db.Column(db.Text)
    raw_desc = db.Column(db.Text)

    location = db.Column(db.String(4096))
    link = db.Column(db.String(4096))
    time = db.Column(db.DateTime)

    games = db.relationship('Game', secondary=event_game_assoc, back_populates='events')
    genres = db.relationship('Genre', secondary=event_genre_assoc, back_populates='direct_events')

    def json(self):
        image = 'https://cf.geekdo-images.com/images/pic1657689_t.jpg'
        if self.games:
            image = self.games[0].image
        elif self.genres:
            image = self.genres[0].image
        return {'id': self.id,
                'name': self.name,
                'img': image,
                'desc': self.desc,
                'location': self.location,
                'time': self.time,
                'games': [(game.id, game.primary_name) for game in self.games],
                'genres': [(genre.id, genre.name) for genre in self.genres],
                'link': self.link
                }
