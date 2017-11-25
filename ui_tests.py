from unittest import main, TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

class TestFrontEnd(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    ##########################
    # SEARCH FRONT-END TESTS #
    ##########################

    # Search with Text Input + Press Return
    def testSearchInputReturn(self):
        driver = self.driver
        driver.get('http://boardgamedb.me')
        self.assertIn('BGDB', driver.title)
        search = driver.find_element_by_name('search-button')
        search.send_keys('apple')
        search.send_keys(Keys.RETURN)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-model'))
        )

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in element.text

    # Search with Text Input + Press Button
    def testSearchInputButton(self):
        driver = self.driver
        driver.get('http://boardgamedb.me')
        self.assertIn('BGDB', driver.title)
        search = driver.find_element_by_name('search-button')
        search.send_keys('apple')
        search_button = driver.find_element_by_class_name('fa-search')
        search_button.click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-model'))
        )

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in element.text

    # Search with URL Query
    def testSearchQuery(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=apple')

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-model'))
        )

        assert 'No Results' not in driver.page_source
        assert 'Apples to Apples' in element.text

    # No Results Search
    def testFailedSearchQuery(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        element = WebDriverWait(driver, 10).until(
            lambda driver: any(elem.text == 'No Results' for elem in driver.find_elements_by_tag_name('h1'))
        )

        assert 'No Results' in driver.page_source

    ################
    # NAVBAR TESTS #
    ################

    # Note: Search functionality of the navbar is tested in the search section

    # Click Logo
    def testNavLogo(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        element = driver.find_element_by_class_name('navbar-brand')
        element.click()

        assert 'https://boardgamedb.me/' == driver.current_url

    # Click Home
    def testNavHome(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'Home':
                elem.click()

        assert 'https://boardgamedb.me/' == driver.current_url

    # Click Games
    def testNavGames(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'Games':
                elem.click()

        assert 'https://boardgamedb.me/games' in driver.current_url

    # Click Genres
    def testNavGenres(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'Genres':
                elem.click()

        assert 'https://boardgamedb.me/genres' in driver.current_url

    # Click Developers
    def testNavDevelopers(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'Developers':
                elem.click()

        assert 'https://boardgamedb.me/developers' in driver.current_url

    # Click Events
    def testNavEvents(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'Events':
                elem.click()

        assert 'https://boardgamedb.me/events' in driver.current_url

    # Click About
    def testNavAbout(self):
        driver = self.driver
        driver.get('https://boardgamedb.me/search?query=zzz123zzz')

        elements = driver.find_elements_by_class_name('nav-link')
        for elem in elements:
            if elem.text == 'About':
                elem.click()

        assert 'https://boardgamedb.me/about' == driver.current_url

if __name__ == "__main__":
    main()
