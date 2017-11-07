from unittest import main, TestCase
from models import db, Game, Family, Genre, Publisher, Artist, Developer, Mechanic, Event
from main import app
from datetime import datetime
from random import randint
import requests
import json

class TestAPI(TestCase):
    games_url = 'http://boardgamedb.me/api/game'
    genres_url = 'http://boardgamedb.me/api/genre'
    developers_url = 'http://boardgamedb.me/api/developer'
    events_url = 'http://boardgamedb.me/api/event'
    headers = {'Content-Type': 'application/json'}

    def setUp(self):
        db.create_all()

    #------
    # Game
    #------
    def test_add_Game1(self):
        
        with app.test_request_context():
            game1 = Game(id=1000000, is_expansion=False, primary_name="game1", alt_names="alt_game1",
                         image="www.test_image.com", desc="This is a test game.", raw_desc="Test game", 
                         year=2000, min_players=0, max_players=1, rating=4.321)
            db.session.add(game1)
            db.session.commit()
            
            gamequery = db.session.query(Game).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.is_expansion, False)
            self.assertEqual(gamequery.primary_name, "game1")
            self.assertEqual(gamequery.alt_names, "alt_game1")
            
            db.session.delete(game1)
            db.session.commit()
            
    def test_add_Game2(self):
        
        with app.test_request_context():
            game2 = Game(id=1000000, is_expansion=True, primary_name="game2", alt_names="alt_game2",
                         image="www.test_image2.com", desc="This is a test game 2.", raw_desc="Test game 2", 
                         year=1997, min_players=2, max_players=4, rating=3.21)
            db.session.add(game2)
            db.session.commit()
            
            gamequery = db.session.query(Game).filter_by(id="1000000").first()
            self.assertEqual(gamequery.image, "www.test_image2.com")
            self.assertEqual(gamequery.desc, "This is a test game 2.")
            self.assertEqual(gamequery.raw_desc, "Test game 2")
            self.assertEqual(gamequery.year, 1997)
            
            db.session.delete(game2)
            db.session.commit()
            
    def test_add_Game3(self):
        
        with app.test_request_context():
            game3 = Game(id=1000000, is_expansion=False, primary_name="game3", alt_names="alt_game3",
                         image="www.test_image3.com", desc="This is a test game 3.", raw_desc="Test game 3",
                         year=1980, min_players=10, max_players=15, rating=2.5)
            db.session.add(game3)
            db.session.commit()
            
            gamequery = db.session.query(Game).filter_by(id="1000000").first()
            self.assertEqual(gamequery.min_players, 10)
            self.assertEqual(gamequery.max_players, 15)
            self.assertEqual(gamequery.rating, 2.5)
            
            db.session.delete(game3)
            db.session.commit()
            
    def test_add_Game4(self):
    
        with app.test_request_context():
            game4 = Game()
            init_len = len(Game.query.all())
            db.session.add(game4)
            db.session.commit()
            changed_len = len(Game.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(game4)
            db.session.commit()
            changed_len = len(Game.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    def test_get_Game1(self):
    
        with app.test_request_context():
            i = randint(1, 99)
            res = requests.get(self.games_url+"/"+str(i), headers=self.headers)
            self.assertEqual(res.status_code, 200)
            json_res = json.loads(res.text)
            db_res = db.session.query(Game).get(i)
            
            self.assertEqual(json_res['id'], db_res.id)
            self.assertEqual(json_res['is_expansion'], db_res.is_expansion)
            self.assertEqual(json_res['name'], db_res.primary_name)
            self.assertEqual(json_res['img'], db_res.image)
            self.assertEqual(json_res['desc'], db_res.desc)
            
    def test_get_Game2(self):
    
        with app.test_request_context():
            i = randint(1, 99)
            res = requests.get(self.games_url+"/"+str(i), headers=self.headers)
            self.assertEqual(res.status_code, 200)
            json_res = json.loads(res.text)
            db_res = db.session.query(Game).get(i)
            
            self.assertEqual(json_res['year'], db_res.year)
            self.assertEqual(json_res['min_players'], db_res.min_players)
            self.assertEqual(json_res['max_players'], db_res.max_players)
            self.assertEqual(json_res['rating'], db_res.rating)
            
    #--------
    # Family
    #--------
    def test_add_Family1(self):
        
        with app.test_request_context():
            family1 = Family(id=1000000, name="family1")
            db.session.add(family1)
            db.session.commit()
            
            gamequery = db.session.query(Family).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "family1")
            
            db.session.delete(family1)
            db.session.commit()
            
    def test_add_Family2(self):
    
        with app.test_request_context():
            family2 = Family()
            init_len = len(Family.query.all())
            db.session.add(family2)
            db.session.commit()
            changed_len = len(Family.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(family2)
            db.session.commit()
            changed_len = len(Family.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #-------
    # Genre
    #-------
    def test_add_Genre1(self):
        
        with app.test_request_context():
            genre1 = Genre(id=1000000, name="genre1", image="www.test_image.com", 
                           desc="This is a test genre.", raw_desc="Test genre")
            db.session.add(genre1)
            db.session.commit()
            
            gamequery = db.session.query(Genre).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "genre1")
            self.assertEqual(gamequery.image, "www.test_image.com")
            self.assertEqual(gamequery.desc, "This is a test genre.")
            self.assertEqual(gamequery.raw_desc, "Test genre")
            
            db.session.delete(genre1)
            db.session.commit()
            
    def test_add_Genre2(self):
    
        with app.test_request_context():
            genre2 = Genre()
            init_len = len(Genre.query.all())
            db.session.add(genre2)
            db.session.commit()
            changed_len = len(Genre.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(genre2)
            db.session.commit()
            changed_len = len(Genre.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #-----------
    # Publisher
    #-----------
    def test_add_Publisher1(self):
        
        with app.test_request_context():
            publisher1 = Publisher(id=1000000, name="publisher1")
            db.session.add(publisher1)
            db.session.commit()
            
            gamequery = db.session.query(Publisher).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "publisher1")
            
            db.session.delete(publisher1)
            db.session.commit()
            
    def test_add_Publisher2(self):
    
        with app.test_request_context():
            publisher2 = Publisher()
            init_len = len(Publisher.query.all())
            db.session.add(publisher2)
            db.session.commit()
            changed_len = len(Publisher.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(publisher2)
            db.session.commit()
            changed_len = len(Publisher.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #--------
    # Artist
    #--------
    def test_add_Artist1(self):
        
        with app.test_request_context():
            artist1 = Artist(id=1000000, name="artist1")
            db.session.add(artist1)
            db.session.commit()
            
            gamequery = db.session.query(Artist).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "artist1")
            
            db.session.delete(artist1)
            db.session.commit()
            
    def test_add_Artist2(self):
    
        with app.test_request_context():
            artist2 = Artist()
            init_len = len(Artist.query.all())
            db.session.add(artist2)
            db.session.commit()
            changed_len = len(Artist.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(artist2)
            db.session.commit()
            changed_len = len(Artist.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #-----------
    # Developer
    #-----------
    def test_add_Developer1(self):
        
        with app.test_request_context():
            developer1 = Developer(id=1000000, name="developer1", image="www.test_image.com", 
                           desc="This is a test developer.", raw_desc="Test developer", website="www.developer.com")
            db.session.add(developer1)
            db.session.commit()
            
            gamequery = db.session.query(Developer).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "developer1")
            self.assertEqual(gamequery.image, "www.test_image.com")
            
            db.session.delete(developer1)
            db.session.commit()
            
    def test_add_Developer2(self):
        
        with app.test_request_context():
            developer2 = Developer(id=1000000, name="developer2", image="www.test_image2.com", 
                           desc="This is a test developer 2.", raw_desc="Test developer 2", website="www.developer2.com")
            db.session.add(developer2)
            db.session.commit()
            
            gamequery = db.session.query(Developer).filter_by(id="1000000").first()
            self.assertEqual(gamequery.desc, "This is a test developer 2.")
            self.assertEqual(gamequery.raw_desc, "Test developer 2")
            self.assertEqual(gamequery.website, "www.developer2.com")
            
            db.session.delete(developer2)
            db.session.commit()
            
    def test_add_Developer3(self):
    
        with app.test_request_context():
            developer3 = Developer()
            init_len = len(Developer.query.all())
            db.session.add(developer3)
            db.session.commit()
            changed_len = len(Developer.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(developer3)
            db.session.commit()
            changed_len = len(Developer.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #----------
    # Mechanic
    #----------
    def test_add_Mechanic1(self):
        
        with app.test_request_context():
            mechanic1 = Mechanic(id=1000000, name="mechanic1")
            db.session.add(mechanic1)
            db.session.commit()
            
            gamequery = db.session.query(Mechanic).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "mechanic1")
            
            db.session.delete(mechanic1)
            db.session.commit()
            
    def test_add_Mechanic2(self):
    
        with app.test_request_context():
            mechanic2 = Mechanic()
            init_len = len(Mechanic.query.all())
            db.session.add(mechanic2)
            db.session.commit()
            changed_len = len(Mechanic.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(mechanic2)
            db.session.commit()
            changed_len = len(Mechanic.query.all())
            self.assertEqual(init_len - 1, changed_len)
            
    #-------
    # Event
    #-------
    def test_add_Event1(self):
        
        with app.test_request_context():
            event1 = Event(id=1000000, name="event1", desc="This is a test event.", raw_desc="Test event",
                           location="event_location", link="www.test_link.com", time=datetime(1864,2,4,0,0))
            db.session.add(event1)
            db.session.commit()
            
            gamequery = db.session.query(Event).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "event1")
            self.assertEqual(gamequery.desc, "This is a test event.")
            self.assertEqual(gamequery.raw_desc, "Test event")
            
            db.session.delete(event1)
            db.session.commit()
            
    def test_add_Event2(self):
        
        with app.test_request_context():
            event2 = Event(id=1000000, name="event2", desc="This is a test event 2.", raw_desc="Test event 2",
                           location="event_location2", link="www.test_link2.com", time=datetime(1980,1,1,5,4))
            db.session.add(event2)
            db.session.commit()
            
            gamequery = db.session.query(Event).filter_by(id="1000000").first()
            self.assertEqual(gamequery.location, "event_location2")
            self.assertEqual(gamequery.link, "www.test_link2.com")
            self.assertEqual(gamequery.time, datetime(1980,1,1,5,4))
            
            db.session.delete(event2)
            db.session.commit()
            
    def test_add_Event3(self):
    
        with app.test_request_context():
            event3 = Event()
            init_len = len(Event.query.all())
            db.session.add(event3)
            db.session.commit()
            changed_len = len(Event.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(event3)
            db.session.commit()
            changed_len = len(Event.query.all())
            self.assertEqual(init_len - 1, changed_len)
    

if __name__ == "__main__":
    main()
