from main import db

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


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    is_expansion = db.Column(db.Boolean)

    primary_name = db.Column(db.String(4096))
    alt_names = db.Column(db.Text)
    
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)

    families = db.relationship('Family', secondary=game_family_assoc, back_populates='games')

    genres = db.relationship('Genre', secondary=game_genre_assoc, back_populates='games')

    year = db.Column(db.Integer)

    publishers = db.relationship('Publisher', secondary=game_publisher_assoc, back_populates='games')

    artists = db.relationship('Artist', secondary=game_artist_assoc, back_populates='games')

    developers = db.relationship('Developer', secondary=game_developer_assoc, back_populates='games')

    mechanics = db.relationship('Mechanic', secondary=game_mechanic_assoc, back_populates='games')

    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)

    rating = db.Column(db.Float)

    def json(self):
        return {'id': self.id,
            'is_expansion': self.is_expansion,
            'name': self.primary_name,
            'alt-names': self.alt_names,
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
                'games': [(game.id, game.name) for game in self.games]
                }


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)

    games = db.relationship('Game', secondary=game_genre_assoc, back_populates='genres')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'desc': self.desc,
                'games': [(game.id, game.name) for game in self.games]
                }

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_publisher_assoc, back_populates='publishers')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.name) for game in self.games]
                }

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_artist_assoc, back_populates='artists')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.name) for game in self.games]
                }

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)

    games = db.relationship('Game', secondary=game_developer_assoc, back_populates='developers')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'desc': self.desc,
                'games': [(game.id, game.name) for game in self.games]
                }

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_mechanic_assoc, back_populates='mechanics')

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'games': [(game.id, game.name) for game in self.games]
                }

map = {'game': Game, 'games': Game,
        'genre': Genre, 'genres': Genre,
        'developer': Developer, 'developers': Developer,
        }
        #'event': Event, 'events': Event}
