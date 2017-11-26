from unittest import main, TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

class TestFrontEnd(TestCase):

    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)

        # Temporary solution for when we get a cached version of the an older
        # version of the website. Basically reload and hope for the best
        # More often than not, the correct version gets loaded
        while True:
            try:
                cls.driver.get('https://boardgamedb.me/developers')
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

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in result.text

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

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in result.text

    # Search with URL Query
    def testSearchQuery(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=apple')

        result = driver.find_element_by_class_name('search-model')

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in result.text

    # No Results Search
    def testFailedSearchQuery(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        element = WebDriverWait(driver, 10).until(
            lambda driver: any(elem.text == 'No Results' for elem in driver.find_elements_by_tag_name('h1'))
        )

        assert 'No Results' in driver.page_source

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

        assert 'https://boardgamedb.me/' == driver.current_url

    # Click Home
    def testNavHome(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-home').click()

        assert 'https://boardgamedb.me/' == driver.current_url

    # Click Games
    def testNavGames(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-games').click()

        assert 'https://boardgamedb.me/games' in driver.current_url

    # Click Genres
    def testNavGenres(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-genres').click()

        assert 'https://boardgamedb.me/genres' in driver.current_url

    # Click Developers
    def testNavDevelopers(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-developers').click()

        assert 'https://boardgamedb.me/developers' in driver.current_url

    # Click Events
    def testNavEvents(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-events').click()

        assert 'https://boardgamedb.me/events' in driver.current_url

    # Click About
    def testNavAbout(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        driver.find_element_by_id('nav-about').click()

        assert 'https://boardgamedb.me/about' == driver.current_url

    ####################
    # Model Grid Pages #
    ####################

    # Pagination is written once for all model grid pages, so we test only once

    # Test << button
    def testPaginationFirst(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-first').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        assert int(queries['page']) == 1

    # Test >> button
    def testPaginationLast(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-last').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        assert int(queries['page']) == 1417

    # Test < button
    def testPaginationPrev(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-prev').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        assert int(queries['page']) == 1

    # Test > button
    def testPaginationNext(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        driver.find_element_by_id('pagination-next').click()

        queries = {query.split('=')[0]: query.split('=')[1]
                for query in driver.current_url.split('?')[1].split('&')}
        assert int(queries['page']) == 3

    # Test numerical page button
    def testPaginationPage(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers?page=2')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'model-link'))
        )

        for page in driver.find_elements_by_id('pagination-page'):
            if page.text == 3:
                page.click()
                queries = {query.split('=')[0]: query.split('=')[1]
                        for query in driver.current_url.split('?')[1].split('&')}
                assert int(queries['page']) == 3

    # Filtering is written once for all model grid pages, so we test only once
    def testFilterUI(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers')

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

        assert found

    # Sorting UI is written once for all grid pages, so we test only once
    def testSortUI(self):
        driver = TestFrontEnd.driver
        driver.get('https://boardgamedb.me/developers')

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

        assert found

    def testGameModels(self):
        pass

    def testGenreModels(self):
        pass

    def testDeveloperModels(self):
        pass

    def testEventModels(self):
        pass

    def testGameModel(self):
        pass

    def testGenreModel(self):
        pass

    def testDeveloperModel(self):
        pass

    def testEventModel(self):
        pass

if __name__ == "__main__":
    main()
