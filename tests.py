from unittest import main, TestCase
from models import db, Game, Family, Genre, Publisher, Artist, Developer, Mechanic
from main import app

class TestAPI(TestCase):
    def setUp(self):
        db.create_all()

    #------
    # Game
    #------
    def test_add_Game1(self):
        
        with app.test_request_context():
            game1 = Game(id=1000000, is_expansion=False, primary_name="game1", alt_names="alt_game1",
                         image="www.test_image.com", desc="This is a test game.", year=2000, 
                         min_players=0, max_players=1, rating=4.321)
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
                         image="www.test_image2.com", desc="This is a test game 2.", year=1997, 
                         min_players=2, max_players=4, rating=3.21)
            db.session.add(game2)
            db.session.commit()
            
            gamequery = db.session.query(Game).filter_by(id="1000000").first()
            self.assertEqual(gamequery.image, "www.test_image2.com")
            self.assertEqual(gamequery.desc, "This is a test game 2.")
            self.assertEqual(gamequery.year, 1997)
            
            db.session.delete(game2)
            db.session.commit()
            
    def test_add_Game3(self):
        
        with app.test_request_context():
            game3 = Game(id=1000000, is_expansion=False, primary_name="game3", alt_names="alt_game3",
                         image="www.test_image3.com", desc="This is a test game 3.", year=1980, 
                         min_players=10, max_players=15, rating=2.5)
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
                           desc="This is a test genre.")
            db.session.add(genre1)
            db.session.commit()
            
            gamequery = db.session.query(Genre).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "genre1")
            self.assertEqual(gamequery.image, "www.test_image.com")
            self.assertEqual(gamequery.desc, "This is a test genre.")
            
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
                           desc="This is a test developer.")
            db.session.add(developer1)
            db.session.commit()
            
            gamequery = db.session.query(Developer).filter_by(id="1000000").first()
            self.assertEqual(gamequery.id, 1000000)
            self.assertEqual(gamequery.name, "developer1")
            self.assertEqual(gamequery.image, "www.test_image.com")
            self.assertEqual(gamequery.desc, "This is a test developer.")
            
            db.session.delete(developer1)
            db.session.commit()
            
    def test_add_Developer2(self):
    
        with app.test_request_context():
            developer2 = Developer()
            init_len = len(Developer.query.all())
            db.session.add(developer2)
            db.session.commit()
            changed_len = len(Developer.query.all())
            self.assertEqual(init_len + 1, changed_len)
            
            init_len = changed_len
            db.session.delete(developer2)
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

if __name__ == "__main__":
    main()
