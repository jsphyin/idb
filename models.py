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

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_family_assoc, back_populates='families')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)

    games = db.relationship('Game', secondary=game_genre_assoc, back_populates='genres')

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_publisher_assoc, back_populates='publishers')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_artist_assoc, back_populates='artists')

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))
    image = db.Column(db.String(4096))
    desc = db.Column(db.Text)

    games = db.relationship('Game', secondary=game_developer_assoc, back_populates='developers')

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(4096))

    games = db.relationship('Game', secondary=game_mechanic_assoc, back_populates='mechanics')