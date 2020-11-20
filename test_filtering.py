import unittest
from main import noFilter
from main import CheckSubstringMatches
from main import ApplyFoundFilters
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
from pymongo import MongoClient
from mongoengine import *

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
boardgameobjects = client["BGDB"].boardgamecollection
genreobjects = client["BGDB"].genrecollection
publisherobjects = client["BGDB"].publishercollection


##################################################BACK END TESTING#########################################################

class TestFiltering(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     print('setupClass')

    # @classmethod
    # def tearDownClass(cls):
    #     print('teardownClass')

    # def setUp(self):
    #     print('setUp')
    #     self.emp_1 = Employee('Corey', 'Schafer', 50000)
    #     self.emp_2 = Employee('Sue', 'Smith', 60000)

    # def tearDown(self):
    #     print('tearDown\n')


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







if __name__ == '__main__':
    unittest.main()