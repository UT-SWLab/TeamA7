import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
class TestsTeamA7(unittest.TestCase):
    #Test Home Carousel takes you to legitimate pages
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
        #for local testing, two options: use flask testing, or open up powershell, run main.py
        #there and run the next line intead of at the deployed app
        #self.driver.get("http://127.0.0.1:5000/")
        self.driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")

    #Tests the home title is correct and logo takes you home from home
    def test_home_view(self):
        navbutton = self.driver.find_element_by_class_name("navbar-brand")
        navbutton.click() #should refresh to home
        self.assertEqual(self.driver.title, 'TeamA7 Project Home')

    #Tests navigation bar results in pages intended and you cannot exit site from navbar
    def test_navbar(self):
        navbutton = self.driver.find_element_by_class_name("navbar-brand")
        navbutton.click() #should refresh to home
        self.assertEqual(self.driver.title, 'TeamA7 Project Home')
        #From Home go to About Page, from About Page go to Home
        about = self.driver.find_element_by_id("aboutnav")
        about.click() #should take you to About Page
        self.assertEqual(self.driver.title, 'TeamA7 Project About Page')
        logobutton = self.driver.find_element_by_class_name("navbar-brand")
        logobutton.click()  # should take you home from About
        self.assertEqual(self.driver.title, 'TeamA7 Project Home')
        #From Home go to All Board Games
        logobutton = self.driver.find_element_by_id("boardgamesnav")
        logobutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games List')

    #Tests that list pages load within 5 seconds
    def test_list_load_time(self):
        #testing board games list generation
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.title, 'Board Games List')
        header_with_page_number = self.driver.find_element(By.TAG_NAME,"h1")
        self.assertEqual(header_with_page_number.text, "Board Games Page 1")
        publisherbutton = self.driver.find_element_by_id("publishersnav")
        publisherbutton.click()  # should take you to Publishers List Page
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.title, 'Board Games Publisher List')
        header_with_page_number = self.driver.find_element(By.TAG_NAME,"h1")
        self.assertEqual(header_with_page_number.text, "Publishers Page 1")
        genresbutton = self.driver.find_element_by_id("genresnav")
        genresbutton.click()  # should take you to Genres List Page
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.title, 'Board Game Genres List')
        header_with_page_number = self.driver.find_element(By.TAG_NAME,"h1")
        self.assertEqual(header_with_page_number.text, "Genres Page 1")

    #Starting from a random game from board game lists page
    def test_model_linking_board_game_list(self):
        #testing board games list generation
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games List')
        games_buttons_on_page = self.driver.find_elements(By.ID,"gamename")
        random_game = games_buttons_on_page[random.randint(0,len(games_buttons_on_page))]
        gamename = random_game.text
        random_game.click()
        self.assertEqual(self.driver.find_element(By.TAG_NAME,'h2').text, gamename)
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games List')
        publisher_buttons_on_page = self.driver.find_elements(By.ID,"publishername")
        random_publisher = publisher_buttons_on_page[random.randint(0,len(publisher_buttons_on_page))]
        publishername = random_publisher.text
        random_publisher.click()
        self.assertEqual("Publisher: " + self.driver.find_element(By.TAG_NAME,'h2').text, publishername)
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games List')

    def test_model_board_game_list(self):
        #testing board games list links
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games List')
        games_buttons_on_page = self.driver.find_elements(By.ID,"gamename") #all games visible on this page
        total_for_page = len(games_buttons_on_page)
        for i in range(0,total_for_page):
            name = games_buttons_on_page[i].text
            games_buttons_on_page[i].click()
            self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
            self.driver.find_element_by_id("boardgamesnav").click()
            games_buttons_on_page = self.driver.find_elements(By.ID,"gamename")

    def test_model_genres_list(self):
        #testing board game genres list generation
        genresbutton = self.driver.find_element_by_id("genresnav")
        genresbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Game Genres List')
        genres_buttons_on_page = self.driver.find_elements(By.ID,"genrename") #all games visible on this page
        total_for_page = len(genres_buttons_on_page)
        for i in range(0,total_for_page):
            name = genres_buttons_on_page[i].text
            genres_buttons_on_page[i].click()
            self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
            self.driver.find_element_by_id("genresnav").click()
            genres_buttons_on_page = self.driver.find_elements(By.ID,"genrename")

    def test_model_publishers_list(self):
        #testing board game publishers list generation
        genresbutton = self.driver.find_element_by_id("publishersnav")
        genresbutton.click()  # should take you to Board games Page
        self.assertEqual(self.driver.title, 'Board Games Publisher List')
        genres_buttons_on_page = self.driver.find_elements(By.ID,"publisherename") #all games visible on this page
        total_for_page = len(genres_buttons_on_page)
        for i in range(0,total_for_page):
            name = genres_buttons_on_page[i].text
            genres_buttons_on_page[i].click()
            self.assertEqual(self.driver.find_element(By.TAG_NAME, 'h2').text, name)
            self.driver.find_element_by_id("publishersnav").click()
            genres_buttons_on_page = self.driver.find_elements(By.ID,"publishername")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
