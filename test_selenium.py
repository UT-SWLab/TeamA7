import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestsTeamA7(unittest.TestCase):
    #Test Home Carousel takes you to legitimate pages
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path= r"C:\Users\sbloe\Desktop\geckodriver.exe")
        #self.driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")
        self.driver.get(r"http://127.0.0.1:5000/")

    #Tests navigation bar results in pages intended and you cannot exit site from navbar
    def test_navbar(self):
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_id("aboutnav").click()
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'TeamA7 Project About Page')
        self.driver.find_element_by_id("boardgamesnav").click()
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'Board Game List')
        #go to All Genres
        self.driver.find_element_by_id("genresnav").click()
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'Board Game Genres List')
        # go to All Publishers
        publishers = self.driver.find_element_by_id("publishersnav")
        publishers.click()
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'Board Game Publishers List')

    def test_model_board_game_list(self):
        #testing board games list pagination and links for default
        self.driver.find_element_by_id("boardgamesnav").click()  # should take you to Board games Page
        self.driver.implicitly_wait(3)
        self.assertEqual(self.driver.title, 'Board Game List')
        #get all pagination buttons, we shall skip first and last as those are previous and next
        pagination_count = len(self.driver.find_elements(By.CLASS_NAME, "page-link"))
        for page in range(0,pagination_count-2):
            self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()
            total_for_page = len(self.driver.find_elements(By.ID,"gamename"))
            for i in range(0, total_for_page):
                name = self.driver.find_elements(By.ID, "gamename")[i].text
                self.driver.find_elements(By.ID, "gamename")[i].click()
                self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
                self.driver.find_element_by_id("boardgamesnav").click()
                self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()

    def test_model_genres_list(self):
        # testing board games genres list pagination and links for default
        genrebutton = self.driver.find_element_by_id("genresnav")
        genrebutton.click()  # should take you to Board Genres Page
        self.assertEqual(self.driver.title, 'Board Game Genres List')
        # get all pagination buttons, we shall skip first and last as those are previous and next
        pagination_count = len(self.driver.find_elements(By.CLASS_NAME, "page-link"))
        for page in range(0, pagination_count - 2):
            self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()
            total_for_page = len(self.driver.find_elements(By.ID, "genrename"))
            for i in range(0, total_for_page):
                name = self.driver.find_elements(By.ID, "genrename")[i].text
                self.driver.find_elements(By.ID, "genrename")[i].click()
                self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
                self.driver.find_element_by_id("genresnav").click()
                self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()

    def test_model_publishers_list(self):
        # testing board games publishers list pagination and links for default
        self.driver.find_element_by_id("publishersnav").click()
        self.assertEqual(self.driver.title, 'Board Game Publishers List')
        # get all pagination buttons, we shall skip first and last as those are previous and next
        pagination_count = len(self.driver.find_elements(By.CLASS_NAME, "page-link"))
        for page in range(0, pagination_count - 2):
            self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()
            total_for_page = len(self.driver.find_elements(By.ID, "publishername"))
            for i in range(0, total_for_page):
                name = self.driver.find_elements(By.ID, "publishername")[i].text
                self.driver.find_elements(By.ID, "publishername")[i].click()
                self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
                self.driver.find_element_by_id("publishersnav").click()
                self.driver.find_elements(By.CLASS_NAME, "page-link")[page].click()


    def tearDown(self):
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
