from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from database import Base


game_family_assoc = Table('GameFamilyAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('family_id', Integer, ForeignKey('Family.id'))
)

game_genre_assoc = Table('GameGenreAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('genre_id', Integer, ForeignKey('Genre.id'))
)

game_publisher_assoc = Table('GamePublisherAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('publisher_id', Integer, ForeignKey('Publisher.id'))
)

game_artist_assoc = Table('GameArtistAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('artist_id', Integer, ForeignKey('Artist.id'))
)

game_developer_assoc = Table('GameDeveloperAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('developer_id', Integer, ForeignKey('Developer.id'))
)

game_mechanic_assoc = Table('GameMechanicAssociation', Base.metadata,
    Column('game_id', Integer, ForeignKey('Game.id')),
    Column('mechanic_id', Integer, ForeignKey('Mechanic.id'))
)


class Game(Base):
    __tablename__ = 'Game'

    id = Column(Integer, primary_key=True)

    is_expansion = Column(Boolean)

    primary_name = Column(String(4096))
    alt_names = Column(String(4096))
    
    image = Column(String(4096))

    description = Column(String(4096))

    families = relationship("Family", secondary=game_family_assoc, back_populates="games")

    genres = relationship("Genre", secondary=game_genre_assoc, back_populates="games")

    year = Column(Integer)

    publishers = relationship("Publisher", secondary=game_publisher_assoc, back_populates="games")

    artists = relationship("Artist", secondary=game_artist_assoc, back_populates="games")

    developers = relationship("Developer", secondary=game_developer_assoc, back_populates="games")

    mechanics = relationship("Mechanic", secondary=game_mechanic_assoc, back_populates="games")

    min_players = Column(Integer)
    max_players = Column(Integer)

    rating = Column(Float)

class Family(Base):
    __tablename__ = 'Family'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    games = relationship("Game", secondary=game_family_assoc, back_populates="families")

class Genre(Base):
    __tablename__ = 'Genre'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    description = Column(String(4096))

    games = relationship("Game", secondary=game_genre_assoc, back_populates="genres")

class Publisher(Base):
    __tablename__ = 'Publisher'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    games = relationship("Game", secondary=game_publisher_assoc, back_populates="publishers")

class Artist(Base):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    games = relationship("Game", secondary=game_artist_assoc, back_populates="artists")

class Developer(Base):
    __tablename__ = 'Developer'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    description = Column(String(4096))

    games = relationship("Game", secondary=game_developer_assoc, back_populates="developers")

class Mechanic(Base):
    __tablename__ = 'Mechanic'

    id = Column(Integer, primary_key=True)

    name = Column(String(4096))

    games = relationship("Game", secondary=game_mechanic_assoc, back_populates="mechanics")
