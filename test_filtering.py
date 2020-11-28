import unittest
from main import noFilter
from main import SelectFilter
from main import ApplyFoundFilters
from selenium import webdriver
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
        for game in SelectFilter("1_Hour_or_More", boardgameobjects).find():
            max_playtime = game["Max_Playtime"]
            self.assertTrue(60 <= max_playtime)

        #1 Hour or Less Filter for Board Games
        for game in SelectFilter("1_Hour_or_Less", boardgameobjects).find():
            min_playtime = game["Min_Playtime"]
            self.assertTrue(60 >= min_playtime)

        #30 Minutes or Less Filter for Board Games
        for game in SelectFilter("30_Minutes_or_Less", boardgameobjects).find():
            min_playtime = game["Min_Playtime"]
            self.assertTrue(30 >= min_playtime)

        #Players: 2 Filter for Board Games
        for game in SelectFilter("Players:_2", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 2 <= max_players)

        #Players: 3 Filter for Board Games
        for game in SelectFilter("Players:_3", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 3 <= max_players)

        #Players: 4 Filter for Board Games
        for game in SelectFilter("Players:_4", boardgameobjects).find():
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 4 <= max_players)

        #Players: 5+ Filter for Board Games
        for game in SelectFilter("Players:_5 +", boardgameobjects).find():
            max_players = game["Max_Players"]
            self.assertTrue(max_players >= 5)

        #AveragePrice: $30 or More Filter for Genres
        for genre in SelectFilter("Average_Price:_$30_or_More", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(30 <= float(average_price))

        #AveragePrice: $30 or Less Filter for Genres
        for genre in SelectFilter("Average_Price:_$30_or_Less", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #AveragePrice: $15 or Less Filter for Genres
        for genre in SelectFilter("Average_Price:_$15_or_Less", genreobjects).find():
            average_price = genre["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Playtime: 30 Minutes or Less Filter for Genres
        for genre in SelectFilter("Average_Playtime:_30_minutes_or_Less", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Genres
        for genre in SelectFilter("Average_Playtime:_1_Hour_or_Less", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Genres
        for genre in SelectFilter("Average_Playtime:_1_Hour_or_More", genreobjects).find():
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Playtime: 30 Minutes or Less Filter for Publishers
        for publisher in SelectFilter("Average_Playtime:_30_minutes_or_Less", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Publishers
        for publisher in SelectFilter("Average_Playtime:_1_Hour_or_Less", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Publishers
        for publisher in SelectFilter("Average_Playtime:_1_Hour_or_More", publisherobjects).find():
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Price: $30 or Less Publisher Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$30_or_Less_Publisher", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #Average Price: $15 or Less Publisher Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$15_or_Less_Publisher", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Price: $30 or More Double Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$30_or_More_Double", publisherobjects).find():
            average_price = publisher["Average_Price"]
            self.assertTrue(30 <= float(average_price))

    # Testing that when no filters are applied, all items in the collection are shown
    def test_correct_no_filter_results(self):
        print("Testing that when no filters are applied, all items in the collection are shown")

        #No Filters for Games
        self.assertEqual(boardgameobjects.count_documents({}), SelectFilter("", boardgameobjects).count_documents({}))

        #No Filters for Genres
        self.assertEqual(genreobjects.count_documents({}), SelectFilter("", genreobjects).count_documents({}))

        #No Filters for Publishers
        self.assertEqual(publisherobjects.count_documents({}), SelectFilter("", publisherobjects).count_documents({}))


##################################################FRONT END TESTING#########################################################

class FilteringWebTest(unittest.TestCase):

    #Tests that filtered game pages load within 5 seconds, and the current filter checkbox (and only that one) is selected once the page loads
    def test_filtered_game_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/nofilters")

        # click dropdown menu for game filters
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()

        #initially, no checkboxes should be checked
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 1 hour or more filter
        driver.execute_script("arguments[0].click();", checkbox1)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/1_Hour_or_More')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertTrue(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 1 hour or less filter
        driver.execute_script("arguments[0].click();", checkbox2)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/1_Hour_or_Less')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertTrue(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 30 minutes or less filter
        driver.execute_script("arguments[0].click();", checkbox3)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/30_Minutes_or_Less')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertTrue(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 2 player filter
        driver.execute_script("arguments[0].click();", checkbox4)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_2')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertTrue(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 3 player filter
        driver.execute_script("arguments[0].click();", checkbox5)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_3')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertTrue(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 4 player filter
        driver.execute_script("arguments[0].click();", checkbox6)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_4')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertTrue(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertFalse(checkbox7.is_selected())

        # click checkbox for 5 player filter
        driver.execute_script("arguments[0].click();", checkbox7)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgames/normal/1/Players:_5%20+')

        # check that ONLY the current filter checkbox is selected
        gamefilters = driver.find_element_by_id("FiltersForGames")
        gamefilters.click()
        checkbox1 = driver.find_element_by_id("checkbox1")
        self.assertFalse(checkbox1.is_selected())
        checkbox2 = driver.find_element_by_id("checkbox2")
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = driver.find_element_by_id("checkbox3")
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = driver.find_element_by_id("checkbox4")
        self.assertFalse(checkbox4.is_selected())
        checkbox5 = driver.find_element_by_id("checkbox5")
        self.assertFalse(checkbox5.is_selected())
        checkbox6 = driver.find_element_by_id("checkbox6")
        self.assertFalse(checkbox6.is_selected())
        checkbox7 = driver.find_element_by_id("checkbox7")
        self.assertTrue(checkbox7.is_selected())

        driver.close()

    #Tests that filtered genre pages load within 5 seconds, and the current filter checkbox (and only that one) is selected once the page loads
    def test_filtered_genre_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/nofilters")

        # click dropdown menu for genre filters
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()

        #initially, no checkboxes should be checked
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertFalse(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertFalse(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertFalse(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertFalse(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertFalse(checkbox12.is_selected())

        # click checkbox for average price: $30 or more filter
        driver.execute_script("arguments[0].click();", checkbox8)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$30_or_More')


        # check that ONLY the current filter checkbox is selected
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertTrue(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertFalse(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertFalse(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertFalse(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertFalse(checkbox12.is_selected())

        # click checkbox for average price: $30 or less filter
        driver.execute_script("arguments[0].click();", checkbox9)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$30_or_Less')

        # check that ONLY the current filter checkbox is selected
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertFalse(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertTrue(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertFalse(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertFalse(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertFalse(checkbox12.is_selected())

        # click checkbox for average price: $15 or less filter
        driver.execute_script("arguments[0].click();", checkbox10)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Price:_$15_or_Less')

        # check that ONLY the current filter checkbox is selected
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertFalse(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertFalse(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertTrue(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertFalse(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertFalse(checkbox12.is_selected())

        # click checkbox for average playtime: 30 minutes or less filter
        driver.execute_script("arguments[0].click();", checkbox11)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Playtime:_30_minutes_or_Less')

        # check that ONLY the current filter checkbox is selected
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertFalse(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertFalse(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertFalse(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertTrue(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertFalse(checkbox12.is_selected())

        # click checkbox for average playtime: 30 minutes or more filter
        driver.execute_script("arguments[0].click();", checkbox12)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamegenres/normal/1/Average_Playtime:_30_Minutes_or_More')

        # check that ONLY the current filter checkbox is selected
        genrefilters = driver.find_element_by_id("FiltersForGenres")
        genrefilters.click()
        checkbox8 = driver.find_element_by_id("checkbox8")
        self.assertFalse(checkbox8.is_selected())
        checkbox9 = driver.find_element_by_id("checkbox9")
        self.assertFalse(checkbox9.is_selected())
        checkbox10 = driver.find_element_by_id("checkbox10")
        self.assertFalse(checkbox10.is_selected())
        checkbox11 = driver.find_element_by_id("checkbox11")
        self.assertFalse(checkbox11.is_selected())
        checkbox12 = driver.find_element_by_id("checkbox12")
        self.assertTrue(checkbox12.is_selected())

        driver.close()

    #Tests that filtered publisher pages load within 5 seconds, and the current filter checkbox (and only that one) is selected once the page loads
    def test_filtered_publisher_page_load_time(self):
        driver = webdriver.Firefox(executable_path=r"/Users/Allegra/Desktop/EE 461L/Tutorial 8/part2/geckodriver")
        driver.get(r"https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/nofilters")

        # click dropdown menu for publisher filters
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()

        # initially, no checkboxes should be checked
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertFalse(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertFalse(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertFalse(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertFalse(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertFalse(checkbox17.is_selected())

        # click checkbox for average price: $30 or more filter
        driver.execute_script("arguments[0].click();", checkbox13)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$30_or_More_Double')

        # check that ONLY the current filter checkbox is selected
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertTrue(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertFalse(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertFalse(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertFalse(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertFalse(checkbox17.is_selected())

        # click checkbox for average price: $30 or less filter
        driver.execute_script("arguments[0].click();", checkbox14)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$30_or_Less_Publisher')

        # check that ONLY the current filter checkbox is selected
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertFalse(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertTrue(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertFalse(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertFalse(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertFalse(checkbox17.is_selected())

        # click checkbox for average price: $15 or less filter
        driver.execute_script("arguments[0].click();", checkbox15)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Price:_$15_or_Less_Publisher')

        # check that ONLY the current filter checkbox is selected
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertFalse(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertFalse(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertTrue(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertFalse(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertFalse(checkbox17.is_selected())

        # click checkbox for average playtime: 30 minutes or less filter
        driver.execute_script("arguments[0].click();", checkbox16)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Playtime:_30_minutes_or_Less')

        # check that ONLY the current filter checkbox is selected
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertFalse(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertFalse(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertFalse(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertTrue(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertFalse(checkbox17.is_selected())

        # click checkbox for average playtime: 30 minutes or more filter
        driver.execute_script("arguments[0].click();", checkbox17)
        # wait for page to load
        time.sleep(5)
        # check that the site routed to the correct page
        self.assertEqual(driver.current_url, 'https://fall-2020-ee461l-teama7.uc.r.appspot.com/boardgamepublishers/normal/1/Average_Playtime:_30_Minutes_or_More')

        # check that ONLY the current filter checkbox is selected
        publisherfilters = driver.find_element_by_id("FiltersForPublisher")
        publisherfilters.click()
        checkbox13 = driver.find_element_by_id("checkbox13")
        self.assertFalse(checkbox13.is_selected())
        checkbox14 = driver.find_element_by_id("checkbox14")
        self.assertFalse(checkbox14.is_selected())
        checkbox15 = driver.find_element_by_id("checkbox15")
        self.assertFalse(checkbox15.is_selected())
        checkbox16 = driver.find_element_by_id("checkbox16")
        self.assertFalse(checkbox16.is_selected())
        checkbox17 = driver.find_element_by_id("checkbox17")
        self.assertTrue(checkbox17.is_selected())

        driver.close()



if __name__ == '__main__':
    unittest.main()