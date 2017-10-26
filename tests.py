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
            

if __name__ == "__main__":
    main()
