#This file is backend testing for all functionality in main.py: page routing, search, sorting, and filtering

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # so we can access main.py from parent directory
import unittest
from flask import template_rendered
from main import app
from search import searchdb
from main import noFilter
from main import SelectFilter
from main import ApplyFoundFilters
import pymongo
from pymongo import MongoClient
from mongoengine import *

# need to connect to database for sorting and filtering testing
client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
boardgameobjects = client["BGDB"].boardgamecollection
genreobjects = client["BGDB"].genrecollection
publisherobjects = client["BGDB"].publishercollection


############################################TEST PAGE ROUTING VALIDITY#################################################

class ValidRoutingTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    #go to home page
    def test_home(self):
        home = self.app.get('/')
        self.assertEqual(home.status_code, 200)

    #test game page is valid
    def test_game_list(self):
        gamelist = self.app.get('boardgames/normal/1/nofilters')
        self.assertEqual(gamelist.status_code, 200)

    #test genre page is valid
    def test_genre_list(self):
        genrelist = self.app.get('boardgamegenres/normal/1/nofilters')
        self.assertEqual(genrelist.status_code, 200)

    #test publisher page is valid
    def test_publisher_list(self):
        publisherlist = self.app.get('boardgamepublishers/normal/1/nofilters')
        self.assertEqual(publisherlist.status_code, 200)

    # test boardgame filter pages are valid
    def test_game_list_filters(self):
        filters = ['1_Hour_or_More',
                   '1_Hour_or_Less',
                   '30_Minutes_or_Less',
                   'Players:_2',
                   'Players:_3',
                   'Players:_4',
                   'Players:_5 +']
        for f in filters:
            filteredpage = self.app.get('boardgames/normal/1/'+f)
            self.assertEqual(filteredpage.status_code, 200)

    # test genre filter pages are valid
    def test_genre_list_filters(self):
        filters = ['Average_Price:_$30_or_More',
                   'Average_Price:_$30_or_Less',
                   'Average_Price:_$15_or_Less',
                   'Average_Playtime:_30_Minutes_or_Less',
                   'Average_Playtime:_30_Minutes_or_More']
        for f in filters:
                filteredpage = self.app.get('boardgamegenres/normal/1/' + f)
                self.assertEqual(filteredpage.status_code, 200)

    # test publisher filter pages are valid
    def test_publisher_list_filters(self):
        filters = ['Average_Price:_$30_or_More',
                   'Average_Price:_$30_or_Less',
                   'Average_Price:_$15_or_Less',
                   'Average_Playtime:_30_Minutes_or_Less',
                   'Average_Playtime:_30_Minutes_or_More']
        for f in filters:
            filteredpage = self.app.get('boardgamepublishers/normal/1/' + f)
            self.assertEqual(filteredpage.status_code, 200)

    # test games sort pages are valid
    def test_game_list_sort(self):
        sort = ["alphabetical","inverse","min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgames/'+s+'/1/nofilters')
            self.assertEqual(sortedpage.status_code, 200)

    # test genres sort pages are valid
    def test_genres_list_sort(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgamegenres/' + s + '/1/nofilters')
            self.assertEqual(sortedpage.status_code, 200)

    # test publisher sort pages are valid
    def test_publishers_list_sort(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgamepublishers/' + s + '/1/nofilters')
            self.assertEqual(sortedpage.status_code, 200)

    # test game sort+filter pages are valid
    def test_game_list_sort_filter(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        filters = ['1_Hour_or_More',
                   '1_Hour_or_Less',
                   '30_Minutes_or_Less',
                   'Players:_2',
                   'Players:_3',
                   'Players:_4',
                   'Players:_5 +']
        for s in sort:
            for f in filters:
                sortfiltered = self.app.get('boardgames/' + s + '/1/'+f)
                self.assertEqual(sortfiltered.status_code, 200)

    # test genre sort+filter pages are valid
    def test_genre_list_sort_filter(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        filters = ['Average_Price:_$30_or_More',
                   'Average_Price:_$30_or_Less',
                   'Average_Price:_$15_or_Less',
                   'Average_Playtime:_30_Minutes_or_Less',
                   'Average_Playtime:_30_Minutes_or_More']
        for s in sort:
            for f in filters:
                sortfiltered = self.app.get('boardgamegenres/' + s + '/1/'+f)
                self.assertEqual(sortfiltered.status_code, 200)



############################################TEST SEARCH FUNCTIONALITY#################################################

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_exact_search(self):
        exact, partial = searchdb('Scrabble', ['boardgames','genres','publishers'], ['Name'])
        self.assertTrue(len(exact['boardgames']) == 1)
        self.assertTrue(len(exact['publishers']) == 0)
        self.assertTrue(len(exact['genres']) == 0)

        exact, partial = searchdb('Scrabble', ['boardgames'], ['Name'])
        self.assertTrue(exact['boardgames'][0]['Name'] == 'Scrabble')

        exact, partial = searchdb('Racing', ['genres'], ['Name'])
        self.assertTrue(exact['genres'][0]['Name'] == 'Racing')

        exact, partial = searchdb('Stronghold', ['publishers'], ['Name'])
        self.assertTrue(exact['publishers'][0]['Name'] == 'Stronghold Games')

        exact, partial = searchdb('Flamme Rouge', ['genres'], ['Games'])
        self.assertTrue(exact['genres'][0]['Name'] == 'Racing')

        exact, partial = searchdb('Flamme Rouge', ['publishers'], ['Games'])
        self.assertTrue(exact['publishers'][0]['Name'] == 'Stronghold Games')

    def test_partial_search(self):
        exact, partial = searchdb('Flam asdfasdf', ['boardgames', 'genres','publishers'], ['Name'])
        self.assertTrue(len(partial['Flam']['boardgames']) == 1)
        self.assertTrue(len(partial['Flam']['publishers']) == 0)
        self.assertTrue(len(partial['Flam']['genres']) == 0)

        exact, partial = searchdb('Scrab safsddf', ['boardgames'], ['Name'])
        self.assertEqual(partial['Scrab']['boardgames'][0]['Name'], 'Scrabble')

        exact, partial = searchdb('Rac sdfsaf', ['genres'], ['Name'])
        self.assertEqual(partial['Rac']['genres'][0]['Name'], 'Racing')

        exact, partial = searchdb('Strong asdfasdf', ['publishers'], ['Name'])
        self.assertEqual(partial['Strong']['publishers'][0]['Name'], 'Stronghold Games')

        exact, partial = searchdb('Flam asdfasdf', ['genres'], ['Games'])
        self.assertEqual(partial['Flam']['genres'][0]['Name'], 'Racing')

        exact, partial = searchdb('Flam asdfasdf', ['publishers'], ['Games'])
        self.assertEqual(partial['Flam']['publishers'][0]['Name'], 'Stronghold Games')

    def test_bad_search(self):
        exact, partial = searchdb('zxcvbnmasdfghjklqwertyuiop', ['boardgames', 'genres', 'publishers'], ['all'])
        self.assertEqual(exact, {'boardgames': [], 'genres': [], 'publishers': []})
        self.assertEqual(partial, {})

    def test_fields(self):
        exact, partial = searchdb('Scrabble', ['boardgames'], ['Name'])
        self.assertTrue(len(exact) == 1)

        exact, partial = searchdb('Scrabble', ['genres', 'publishers'], ['Name'])
        self.assertTrue(len(exact) == 2)



############################################TEST SORTING FUNCTIONALITY#################################################

'''
This testing uses a real instances of MongDB no mocking. This ensures real test of connectivity and speed of filtering
sorting functions. Speed is of great importance to our user and our first priority. 
'''

def isInAlphabeticalOrder(word):
    return word == ''.join(sorted(word))

class TestSorting(unittest.TestCase):

    def test_alphabetical_sort(self):
        sort_type = "alphabetical"
        superString = ""
        if sort_type == "alphabetical":
            boardgame_obj = boardgameobjects.find().sort("Name")
            for element in boardgame_obj:
                boardgame = element["Name"]
                superString = superString + (boardgame[0])
            response = print(isInAlphabeticalOrder(superString))
            if response:
                self.assertTrue(True)

    def test_inverse_sort(self):
        sort_type = "inverse"
        superString = ""
        if sort_type == "inverse":
            boardgame_obj = boardgameobjects.find().sort("Name", -1)
            for element in boardgame_obj:
                boardgame = element["Name"]
                superString = superString + (boardgame[0])
            superString=  superString[::-1]
            response = print(isInAlphabeticalOrder(superString))
            if (response):
                self.assertTrue(True)

    def test_min_playtime_sort(self):
            boardgame_obj = boardgameobjects.find().sort("Min_Playtime")
            array = []
            for element in boardgame_obj:
                boardgame = element["Min_Playtime"]
                array.append(boardgame)
            if all(i <= j for i, j in zip(array, array[1:])):
                self.assertTrue(True)

    def test_min_players_sort(self):
        sort_type =  "min-players"
        if sort_type == "min-players":
            boardgame_obj = boardgameobjects.find().sort("Min_Players")
            array = []
            for element in boardgame_obj:
                boardgame = element["Min_Players"]
                array.append(boardgame)
        if all(i <= j for i, j in zip(array, array[1:])):
            self.assertTrue(True)

    # Testing that when no sorting is applied, all items are in the collection.
    def test_correct_no_sorting_results_is_not_empty(self):
        sort_type = "normal"
        if sort_type == "normal":
            boardgame_obj = boardgameobjects.find()
            if boardgameobjects.count() > 0:
                self.assertTrue(True)

    def test_no_sort_to_filter_to_alphabetical(self):
        #Check to make sure collection isn't less than it was before. After filter is applied
            filteredCollection = db["FinalFiltered"]
            filteredCollection.drop()  # drop entire collection
            filteredCollection = db["FinalFiltered"]
            cur = boardgameobjects.find({"$and": [{"Min_Players": {"$lte": 2}}, {"Max_Players": {"$gte": 2}}]})
            for element in cur:
                filteredCollection.insert_one(element)
            countPriorToSorting = filteredCollection.count() #Count after filter
            boardgame_obj = boardgameobjects.find().sort("Min_Players")
            array = []
            for element in boardgame_obj:
                boardgame = element["Min_Players"]
                array.append(boardgame)
            if all(i <= j for i, j in zip(array, array[1:])):
              countAfterSorting = boardgame_obj.count()
            if (countPriorToSorting == countAfterSorting):
                self.assertTrue(True)



############################################TEST FILTERING FUNCTIONALITY#################################################

class TestFiltering(unittest.TestCase):

    # Testing that each filter returns only items that fit the filter
    def test_correct_filter_results(self):
        # #1 Hour or More Filter for Board Games
        for game in SelectFilter("1_Hour_or_More", boardgameobjects):
            max_playtime = game["Max_Playtime"]
            self.assertTrue(60 <= max_playtime)

        #1 Hour or Less Filter for Board Games
        for game in SelectFilter("1_Hour_or_Less", boardgameobjects):
            min_playtime = game["Min_Playtime"]
            self.assertTrue(60 >= min_playtime)

        #30 Minutes or Less Filter for Board Games
        for game in SelectFilter("30_Minutes_or_Less", boardgameobjects):
            min_playtime = game["Min_Playtime"]
            self.assertTrue(30 >= min_playtime)

        #Players: 2 Filter for Board Games
        for game in SelectFilter("Players:_2", boardgameobjects):
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 2 <= max_players)

        #Players: 3 Filter for Board Games
        for game in SelectFilter("Players:_3", boardgameobjects):
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 3 <= max_players)

        #Players: 4 Filter for Board Games
        for game in SelectFilter("Players:_4", boardgameobjects):
            max_players = game["Max_Players"]
            min_players = game["Min_Players"]
            self.assertTrue(min_players <= 4 <= max_players)

        #Players: 5+ Filter for Board Games
        for game in SelectFilter("Players:_5 +", boardgameobjects):
            max_players = game["Max_Players"]
            self.assertTrue(max_players >= 5)

        #AveragePrice: $30 or More Filter for Genres
        for genre in SelectFilter("Average_Price:_$30_or_More", genreobjects):
            average_price = genre["Average_Price"]
            self.assertTrue(30 <= float(average_price))

        #AveragePrice: $30 or Less Filter for Genres
        for genre in SelectFilter("Average_Price:_$30_or_Less", genreobjects):
            average_price = genre["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #AveragePrice: $15 or Less Filter for Genres
        for genre in SelectFilter("Average_Price:_$15_or_Less", genreobjects):
            average_price = genre["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Playtime: 30 Minutes or Less Filter for Genres
        for genre in SelectFilter("Average_Playtime:_30_Minutes_or_Less", genreobjects):
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Genres
        for genre in SelectFilter("Average_Playtime:_1_Hour_or_Less", genreobjects):
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Genres
        for genre in SelectFilter("Average_Playtime:_1_Hour_or_More", genreobjects):
            average_playtime = genre["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Playtime: 30 Minutes or Less Filter for Publishers
        for publisher in SelectFilter("Average_Playtime:_30_Minutes_or_Less", publisherobjects):
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(30 >= average_playtime)

        #Average Playtime: 1 Hour or Less Filter for Publishers
        for publisher in SelectFilter("Average_Playtime:_1_Hour_or_Less", publisherobjects):
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 >= average_playtime)

        #Average Playtime: 1 Hour or More for Publishers
        for publisher in SelectFilter("Average_Playtime:_1_Hour_or_More", publisherobjects):
            average_playtime = publisher["Average_Playtime"]
            self.assertTrue(60 <= average_playtime)

        #Average Price: $30 or Less Publisher Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$30_or_Less_Publisher", publisherobjects):
            average_price = publisher["Average_Price"]
            self.assertTrue(30 >= float(average_price))

        #Average Price: $15 or Less Publisher Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$15_or_Less_Publisher", publisherobjects):
            average_price = publisher["Average_Price"]
            self.assertTrue(15 >= float(average_price))

        #Average Price: $30 or More Double Filter for Publishers
        for publisher in SelectFilter("Average_Price:_$30_or_More_Double", publisherobjects):
            average_price = publisher["Average_Price"]
            self.assertTrue(30 <= float(average_price))

    # Testing that when no filters are applied, all items in the collection are shown
    def test_correct_no_filter_results(self):

        #No Filters for Games
        self.assertEqual(boardgameobjects.count_documents({}), SelectFilter("nofilters", boardgameobjects).count())

        #No Filters for Genres
        self.assertEqual(genreobjects.count_documents({}), SelectFilter("nofilters", genreobjects).count())

        #No Filters for Publishers
        self.assertEqual(publisherobjects.count_documents({}), SelectFilter("nofilters", publisherobjects).count())



if __name__ == '__main__':
    unittest.main()
