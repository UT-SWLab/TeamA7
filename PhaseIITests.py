import unittest
from flask import abort, url_for
from flask_testing import TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestsTeamA7(unittest.TestCase):
    #Test Home Carousel takes you to legitimate pages
    def test_carousel(self):
        #Test Games Carousel
        driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")

    #Tests the home title is correct and logo takes you home from home
    def test_home_view(self):
        driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")
        self.assertEqual(driver.title, 'TeamA7 Project Home')
        driver.close()  # close the browser window

    #Tests navigation bar results in pages intended and you cannot exit site from navbar
    def test_navbar(self):
        driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")
        navbutton = driver.find_element_by_class_name("navbar-brand")
        navbutton.click() #should refresh to home
        self.assertEqual(driver.title, 'TeamA7 Project Home')
        #From Home go to About Page, from About Page go to Home
        logobutton = driver.find_element_by_id("aboutnav")
        logobutton.click() #should take you to About Page
        self.assertEqual(driver.title, 'TeamA7 Project About Page')
        logobutton = driver.find_element_by_class_name("navbar-brand")
        logobutton.click()  # should take you home from About
        self.assertEqual(driver.title, 'TeamA7 Project Home')
        #From Home go to All Board Games
        logobutton = driver.find_element_by_id("boardgamesnav")
        logobutton.click()  # should take you to Board games Page
        self.assertEqual(driver.title, 'Board Games List')
        driver.close()  # close the browser window

    #Tests that list pages load within 10 seconds
    def test_list_load_time(self):
        driver = webdriver.Firefox(executable_path=r"C:\Users\sbloe\Desktop\geckodriver.exe")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/")
        #testing board games list generation
        logobutton = driver.find_element_by_id("boardgamesnav")
        logobutton.click()  # should take you to Board games Page
        driver.implicitly_wait(1)
        self.assertEqual(driver.title, 'Board Games List')
        driver.close()  # close the browser window
if __name__ == '__main__':
    unittest.main()
