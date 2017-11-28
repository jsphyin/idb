from unittest import main, TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

"""
NOTE:
- Requirements to run:
    - Selenium for Python
    - Geckodriver
    - Firefox
"""

class TestFrontEnd(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)

        # Temporary solution for when we get a cached version of the an older
        # version of the website. Basically reload and hope for the best
        # More often than not, the correct version gets loaded
        while True:
            try:
                cls.driver.get('http://boardgamedb.me/developers')
                cls.driver.find_element_by_id('filter-dropdown')
                break
            except:
                cls.driver.quit()
                cls.driver = webdriver.Firefox()
                cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    ##########################
    # SEARCH FRONT-END TESTS #
    ##########################

    # Search with Text Input + Press Return
    def testSearchInputReturn(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me')
        self.assertIn('BGDB', driver.title)
        search = driver.find_element_by_name('query')
        search.send_keys('apple')
        search.send_keys(Keys.RETURN)

        result = driver.find_element_by_class_name('search-model')

        self.assertTrue('No Results' not in driver.page_source)
        self.assertTrue('Apples to Apples' in result.text)

    # Search with Text Input + Press Button
    def testSearchInputButton(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me')
        self.assertIn('BGDB', driver.title)
        search = driver.find_element_by_name('query')
        search.send_keys('apple')
        search_button = driver.find_element_by_id('search-button')
        search_button.click()

        result = driver.find_element_by_class_name('search-model')

        self.assertTrue('No Results' not in driver.page_source)
        self.assertTrue('Apples to Apples' in result.text)

    # Search with URL Query
    def testSearchQuery(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/search?query=apple')

        result = driver.find_element_by_class_name('search-model')

        self.assertTrue('No Results' not in driver.page_source)
        self.assertTrue('Apples to Apples' in result.text)

    # No Results Search
    def testFailedSearchQuery(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        element = WebDriverWait(driver, 10).until(
            lambda driver: any(elem.text == 'No Results' for elem in driver.find_elements_by_tag_name('h1'))
        )

        self.assertTrue('No Results' in driver.page_source)

    ################
    # NAVBAR TESTS #
    ################

    """
    Notes:
    - Search functionality of the navbar is tested in the search section
    - Navbar is written once for all pages, so it can be tested from any source
      page. Empty search is used because it would load the fastest
    """

    # Click Logo
    def testNavLogo(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-logo').click()

        self.assertTrue('https://boardgamedb.me/' == driver.current_url)

    # Click Home
    def testNavHome(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-home').click()

        self.assertTrue('https://boardgamedb.me/' == driver.current_url)

    # Click Games
    def testNavGames(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-games').click()

        self.assertTrue('https://boardgamedb.me/games' in driver.current_url)

    # Click Genres
    def testNavGenres(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-genres').click()

        self.assertTrue('https://boardgamedb.me/genres' in driver.current_url)

    # Click Developers
    def testNavDevelopers(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-developers').click()

        self.assertTrue('https://boardgamedb.me/developers' in driver.current_url)

    # Click Events
    def testNavEvents(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-events').click()

        self.assertTrue('https://boardgamedb.me/events' in driver.current_url)

    # Click About
    def testNavAbout(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-about').click()

        self.assertTrue('https://boardgamedb.me/about' == driver.current_url)

    ####################
    # Model Grid Pages #
    ####################

    # Pagination is written once for all model grid pages, so we test only once

    # Test << button
    def testPaginationFirst(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-first').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        self.assertTrue(int(queries['page']) == 1)

    # Test >> button
    def testPaginationLast(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-last').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        self.assertTrue(int(queries['page']) == 1417)

    # Test < button
    def testPaginationPrev(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-prev').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        self.assertTrue(int(queries['page']) == 1)

    # Test > button
    def testPaginationNext(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-next').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        self.assertTrue(int(queries['page']) == 3)

    # Test numerical page button
    def testPaginationPage(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        for page in driver.find_elements_by_id('pagination-page'):
            if page.text == 3:
                page.click()
                queries = {query.split('=')[0]: query.split('=')[1]
                        for query in driver.current_url.split('?')[1].split('&')}
                self.assertTrue(int(queries['page']) == 3)

    # Filtering is written once for all model grid pages, so we test only once
    def testFilterUI(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers')

        driver.find_element_by_id('filter-dropdown').click()

        for item in driver.find_elements_by_id('filter-type'):
            if item.text == 'Genre':
                item.click()

        filters = driver.find_element_by_class_name('Select-input')
        filters.click()
        filters.send_keys('Card')
        filters.send_keys(Keys.RETURN)

        sleep(2)

        found = False
        for card in driver.find_elements_by_class_name('model-name'):
            if card.text == 'Aaron Brosman':
                found = True

        self.assertTrue(found)

    # Sorting UI is written once for all grid pages, so we test only once
    def testSortUI(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers')

        driver.find_element_by_id('sort-dropdown').click()
        for item in driver.find_elements_by_id('sort-type'):
            if item.text == 'Name ↑':
                item.click()
                break

        sleep(2)

        found = False
        for card in driver.find_elements_by_class_name('model-name'):
            if card.text == '황소망':
                found = True

        self.assertTrue(found)

    # Check games page -> game page
    def testGameModelsImg(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/games')

        game_name = driver.find_element_by_class_name('model-name').text

        driver.find_element_by_id('model-link').click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    # Check games page -> dev page
    def testGameModelsDev(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/games')

        dev = driver.find_element_by_link_text('Bryan M. Simmons')
        dev_name = dev.text
        dev.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == dev_name)

    # Check genres page -> genre page
    def testGenreModelsImg(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/genres')

        genre_name = driver.find_element_by_class_name('model-name').text

        driver.find_element_by_id('model-link').click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == genre_name)

    # Check genres page -> dev page
    def testGenreModelsDev(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/genres')

        dev = driver.find_element_by_link_text('Dr. Reiner Knizia')
        dev_name = dev.text
        dev.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == dev_name)

    # Check genres page -> game page
    def testGenreModelsGame(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/genres')

        game = driver.find_element_by_link_text('Samurai')
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    # Check developers page -> dev page
    def testDeveloperModelsImg(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers')

        developer_name = driver.find_element_by_class_name('model-name').text

        driver.find_element_by_id('model-link').click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == developer_name)

    # Check developers page -> game page
    def testDeveloperModelsGame(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers')

        game = driver.find_element_by_link_text("Liar's Dice")
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    # Check developers page -> genre page
    def testDeveloperModelsGenre(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/developers')

        genre = driver.find_element_by_link_text("Dice")
        genre_name = genre.text
        genre.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == genre_name)

    # Check events page -> event page
    def testEventModelsImg(self):
        driver = TestFrontEnd.driver
        driver.get('http://boardgamedb.me/events')

        event_name = driver.find_element_by_class_name('model-name').text

        driver.find_element_by_id('model-link').click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == event_name)

    # Check events page -> game page
    def testEventModelsGame(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/events')
        game = driver.find_element_by_link_text("Via Nebula")
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    ##############################
    # MODEL PAGE FRONT-END TESTS #
    ##############################

    # Check game page -> dev page
    def testGameModelDev(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/game/190608')
        dev = driver.find_element_by_link_text("Bryan M. Simmons")
        dev_name = dev.text
        dev.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == dev_name)

    # Check game page -> genre page
    def testGameModelGenre(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/game/190608')
        genre = driver.find_element_by_link_text("Card Game")
        genre_name = genre.text
        genre.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == genre_name)

    # Check genre page -> dev page
    def testGenreModelDev(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/genre/1009')
        dev = driver.find_element_by_link_text("Dr. Reiner Knizia")
        dev_name = dev.text
        dev.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == dev_name)

    # Check genre page -> game page
    def testGenreModelGame(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/genre/1009')
        game = driver.find_element_by_link_text("Samurai")
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    # Check developer page -> game page
    def testDeveloperModelGame(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/developer/3')
        game = driver.find_element_by_link_text("Liar's Dice")
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

    # Check developer page -> genre page
    def testDeveloperModelGenre(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/developer/3')
        genre = driver.find_element_by_link_text("Dice")
        genre_name = genre.text
        genre.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == genre_name)

    # Check event page -> game page
    def testEventModelGame(self):
        driver = TestFrontEnd.driver

        driver.get('http://boardgamedb.me/event/765')
        game = driver.find_element_by_link_text("Via Nebula")
        game_name = game.text
        game.click()

        sleep(2)

        self.assertTrue(driver.find_element_by_class_name('model-name').text == game_name)

if __name__ == "__main__":
    main()
