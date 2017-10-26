from unittest import main, TestCase
from models import db, Game, Family, Genre, Publisher, Artist, Developer, Mechanic
from main import app

class TestAPI(TestCase):
    def test_add_Game1(self):
        
        with app.test_request_context():
            db.create_all()

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

if __name__ == "__main__":
    main()
