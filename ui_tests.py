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

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    main()
