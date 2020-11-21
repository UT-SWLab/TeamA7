import unittest
from main import noFilter
from main import CheckSubstringMatches
from main import ApplyFoundFilters
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
from pymongo import MongoClient
from mongoengine import *
import time

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
boardgameobjects = client["BGDB"].boardgamecollection
genreobjects = client["BGDB"].genrecollection
publisherobjects = client["BGDB"].publishercollection


##################################################BACK END TESTING#########################################################

class TestFiltering(unittest.TestCase):


    # Testing that each filter returns only items that fit the filter
    def test_correct_filter_results(self):
        print('Testing that each filter returns only items that fit the filter')
        # #1 Hour or More Filter for Board Games
        for game in CheckSubstringMatches("1_Hour_or_More", boardgameobjects).find():
            max_playtime = game["Max_Playtime"]
            self.assertTrue(60 <= max_playtime)

        #1 Hour or Less Filter for Board Games
        for game in CheckSubstringMatches("1_Hour_or_Less", boardgameobjects).find():
            min_playtime = game["Min_Playtime"]
            self.assertTrue(60 >= min_playtime)

        #30 Minutes or Less Filter for Board Games
        for game in CheckSubstringMatches("30_Minutes_or_Less", boardgameobjects).find():
            min_playtime = game["Min_Playtime"]
            self.assertTrue(30 >= min_playtime)

        #Players: 2 Filter for Board Games
        for game in CheckSubstringMatches("Players:_2", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 2 <= max_players)

        #Players: 3 Filter for Board Games
        for game in CheckSubstringMatches("Players:_3", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 3 <= max_players)

        #Players: 4 Filter for Board Games
        for game in CheckSubstringMatches("Players:_4", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 4 <= max_players)

        #Players: 5+ Filter for Board Games
        for game in CheckSubstringMatches("Players:_5 +", boardgameobjects).find():
            max_players = game["Max_Players"]
            self.assertTrue(max_players >= 5)

        #AveragePrice: $30 or More Filter for Genres
        for genre in CheckSubstringMatches("Average_Price:_$30_or_More", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(30 <= float(average_price))

        #AveragePrice: $30 or Less Filter for Genres
        for genre in CheckSubstringMatches("Average_Price:_$30_or_Less", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #AveragePrice: $15 or Less Filter for Genres
        for genre in CheckSubstringMatches("Average_Price:_$15_or_Less", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Playtime: 30 Minutes or Less Filter for Genres
        for genre in CheckSubstringMatches("Average_Playtime:_30_minutes_or_Less", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Genres
        for genre in CheckSubstringMatches("Average_Playtime:_1_Hour_or_Less", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Genres
        for genre in CheckSubstringMatches("Average_Playtime:_1_Hour_or_More", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Playtime: 30 Minutes or Less Filter for Publishers
        for publisher in CheckSubstringMatches("Average_Playtime:_30_minutes_or_Less", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Publishers
        for publisher in CheckSubstringMatches("Average_Playtime:_1_Hour_or_Less", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Publishers
        for publisher in CheckSubstringMatches("Average_Playtime:_1_Hour_or_More", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Price: $30 or Less Publisher Filter for Publishers
        for publisher in CheckSubstringMatches("Average_Price:_$30_or_Less_Publisher", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #Average Price: $15 or Less Publisher Filter for Publishers
        for publisher in CheckSubstringMatches("Average_Price:_$15_or_Less_Publisher", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Price: $30 or More Double Filter for Publishers
        for publisher in CheckSubstringMatches("Average_Price:_$30_or_More_Double", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(30 <= float(average_price))

    # Testing that when no filters are applied, all items in the collection are shown
    def test_correct_no_filter_results(self):
        print("Testing that when no filters are applied, all items in the collection are shown")

        #No Filters for Games
        self.assertEqual(boardgameobjects.count_documents({}), CheckSubstringMatches("", boardgameobjects).count_documents({}))

        #No Filters for Genres
        self.assertEqual(genreobjects.count_documents({}), CheckSubstringMatches("", genreobjects).count_documents({}))

        #No Filters for Publishers
        self.assertEqual(publisherobjects.count_documents({}), CheckSubstringMatches("", publisherobjects).count_documents({}))


##################################################FRONT END TESTING#########################################################

class FilteringWebTest(unittest.TestCase):
#     # check that the correct checkbox is selected for the current filter being applied
#     def test0(self):
#         driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
#         driver.get(r"file:/Users/Allegra/Desktop/TeamA7/templates/list_base.html")
#         WebElement checkbox1 = driver.findElement(By.id("checkbox1"));
#         System.out.println("The checkbox is selection state is - " + checkbox1.isSelected());
#         self.assertFalse(checkbox1.isSelected())
#         driver.close() # close the browser window


    #Tests that filtered game pages load within 5 seconds
    def test_filtered_game_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/nofilters")

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 1 hour or more filter
        checkbox1 = driver.find_element_by_id("checkbox1")
        driver.execute_script("arguments[0].click();", checkbox1)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/1_Hour_or_More')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 1 hour or less filter
        checkbox2 = driver.find_element_by_id("checkbox2")
        driver.execute_script("arguments[0].click();", checkbox2)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/1_Hour_or_Less')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 30 minutes or less filter
        checkbox3 = driver.find_element_by_id("checkbox3")
        driver.execute_script("arguments[0].click();", checkbox3)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/30_Minutes_or_Less')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 2 player filter
        checkbox4 = driver.find_element_by_id("checkbox4")
        driver.execute_script("arguments[0].click();", checkbox4)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_2')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 3 player filter
        checkbox5 = driver.find_element_by_id("checkbox5")
        driver.execute_script("arguments[0].click();", checkbox5)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_3')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 4 player filter
        checkbox6 = driver.find_element_by_id("checkbox6")
        driver.execute_script("arguments[0].click();", checkbox6)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_4')

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        # click checkbox for 5 player filter
        checkbox7 = driver.find_element_by_id("checkbox7")
        driver.execute_script("arguments[0].click();", checkbox7)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_5%20+')

        driver.close()

    #Tests that filtered genre pages load within 5 seconds
    def test_filtered_genre_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/nofilters")

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForGenres")
        gamefilters.click()
        # click checkbox for 1 hour or more filter
        checkbox8 = driver.find_element_by_id("checkbox8")
        driver.execute_script("arguments[0].click();", checkbox8)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$30_or_More')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForGenres")
        gamefilters.click()
        # click checkbox for 1 hour or less filter
        checkbox9 = driver.find_element_by_id("checkbox9")
        driver.execute_script("arguments[0].click();", checkbox9)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$30_or_Less')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForGenres")
        gamefilters.click()
        # click checkbox for 30 minutes or less filter
        checkbox10 = driver.find_element_by_id("checkbox10")
        driver.execute_script("arguments[0].click();", checkbox10)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$15_or_Less')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForGenres")
        gamefilters.click()
        # click checkbox for 2 player filter
        checkbox11 = driver.find_element_by_id("checkbox11")
        driver.execute_script("arguments[0].click();", checkbox11)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Playtime:_30_minutes_or_Less')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForGenres")
        gamefilters.click()
        # click checkbox for 3 player filter
        checkbox12 = driver.find_element_by_id("checkbox12")
        driver.execute_script("arguments[0].click();", checkbox12)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Playtime:_30_Minutes_or_More')

        driver.close()

    #Tests that filtered publisher pages load within 5 seconds
    def test_filtered_publisher_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/nofilters")

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForPublisher")
        gamefilters.click()
        # click checkbox for 1 hour or more filter
        checkbox13 = driver.find_element_by_id("checkbox13")
        driver.execute_script("arguments[0].click();", checkbox13)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$30_or_More_Double')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForPublisher")
        gamefilters.click()
        # click checkbox for 1 hour or less filter
        checkbox14 = driver.find_element_by_id("checkbox14")
        driver.execute_script("arguments[0].click();", checkbox14)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$30_or_Less_Publisher')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForPublisher")
        gamefilters.click()
        # click checkbox for 30 minutes or less filter
        checkbox15 = driver.find_element_by_id("checkbox15")
        driver.execute_script("arguments[0].click();", checkbox15)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$15_or_Less_Publisher')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForPublisher")
        gamefilters.click()
        # click checkbox for 2 player filter
        checkbox16 = driver.find_element_by_id("checkbox16")
        driver.execute_script("arguments[0].click();", checkbox16)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Playtime:_30_minutes_or_Less')

        # click dropdown menu for genre filters
        gamefilters = driver.find_element_by_id("FiltersForPublisher")
        gamefilters.click()
        # click checkbox for 3 player filter
        checkbox17 = driver.find_element_by_id("checkbox17")
        driver.execute_script("arguments[0].click();", checkbox17)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Playtime:_30_Minutes_or_More')

        driver.close()



if __name__ == '__main__':
    unittest.main()