import unittest
from flask import abort, url_for
from flask_testing import TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
class TestsTeamA7(unittest.TestCase):
    #Test Home Carousel takes you to legitimate pages
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
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
        publisherbutton = self.driver.find_element_by_id("publishersnav")
        publisherbutton.click()  # should take you to Publishers List Page
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.title, 'Board Games Genre List')
        header_with_page_number = self.driver.find_element(By.TAG_NAME,"h1")
        self.assertEqual(header_with_page_number.text, "Publishers Page 1")
    #Tests that
    def test_list_load_time(self):
        #testing board games list generation
        gamesbutton = self.driver.find_element_by_id("boardgamesnav")
        gamesbutton.click()  # should take you to Board games Page
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.title, 'Board Games List')
        header_with_page_number = self.driver.find_element(By.TAG_NAME,"h1")
        self.assertEqual(header_with_page_number.text, "Board Games Page 1")
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
