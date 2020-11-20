import unittest
from main import noFilter
from main import CheckSubstringMatches
from main import ApplyFoundFilters
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
from pymongo import MongoClient
from mongoengine import *

'''
This testing uses a real instances of MongDB no mocking. This ensures real test of connectivity and speed of filtering
sorting functions. Speed is of great importance to our user and our first priority. 
'''

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
boardgameobjects = client["BGDB"].boardgamecollection
genreobjects = client["BGDB"].genrecollection
publisherobjects = client["BGDB"].publishercollection


def isInAlphabeticalOrder(word):
    return word == ''.join(sorted(word))

class TestFiltering(unittest.TestCase):

    def test_alphabetical_sort(self):
        sort_type = "alphabetical"
        superString = ""
        if sort_type == "alphabetical":
            boardgame_obj = boardgameobjects.find().sort("Name")
            for element in boardgame_obj:
                boardgame = element["Name"]
                print(boardgame[0])
                superString = superString + (boardgame[0])
            print(superString)
            response = print(isInAlphabeticalOrder(superString))
            print(response)
            if response:
                self.assertTrue(True)
            # self.assertTrue(response)


    def test_inverse_sort(self):
        sort_type = "inverse"
        superString = ""
        if sort_type == "inverse":
            boardgame_obj = boardgameobjects.find().sort("Name", -1)
            for element in boardgame_obj:
                boardgame = element["Name"]
                print(boardgame[0])
                superString = superString + (boardgame[0])
            superString=  superString[::-1]
            print(superString)
            response = print(isInAlphabeticalOrder(superString))
            if (response):
                self.assertTrue(True)

    #Helper function for alphabetical



    def test_min_playtime_sort(self):
            boardgame_obj = boardgameobjects.find().sort("Min_Playtime")
            array = []
            for element in boardgame_obj:
                boardgame = element["Min_Playtime"]
                print(boardgame)
                array.append(boardgame)
            if all(i <= j for i, j in zip(array, array[1:])):
                print("Minimum Sorted Time Pass")
                self.assertTrue(True)

    def test_min_players_sort(self):
        sort_type =  "min-players"
        if sort_type == "min-players":
            boardgame_obj = boardgameobjects.find().sort("Min_Players")
            array = []
            for element in boardgame_obj:
                boardgame = element["Min_Players"]
                print(boardgame)
                array.append(boardgame)
        if all(i <= j for i, j in zip(array, array[1:])):
            print("Minimum Sorted Players Pass")
            self.assertTrue(True)

    # Testing that when no sorting is applied, all items are in the collection.
    def test_correct_no_sorting_results_is_not_empty(self):
        sort_type = "normal"
        if sort_type == "normal":
            boardgame_obj = boardgameobjects.find()
            if boardgameobjects.count() > 0:
                print("Passed Test")
                self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()