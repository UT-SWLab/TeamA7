import unittest
from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re
client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
board_game_objects = client["BGDB"].boardgamecollection
genre_objects = client["BGDB"].genrecollection
publish_objects = client["BGDB"].publishercollection


class DBTest(unittest.TestCase):
    def test_noEmptyEntries(self):
        for g in board_game_objects.find():
            self.assertNotEqual(g["Name"], "")
        for g in genre_objects.find():
            self.assertNotEqual(g["Name"], "")
        for p in publish_objects.find():
            self.assertNotEqual(p["Name"], "")
    def test_games_connect_to_other_models(self):
        for g in board_game_objects.find():
            genres = g["genres"]
            for gen in genres:
                self.assertNotEqual(genre_objects.find({"Name": gen}), None)
            publisher = g["Publisher"]
            self.assertNotEqual(publish_objects.find({"Name": publisher}), None)
    def test_genres_connect_to_other_models(self):
        for g in genre_objects.find():
            games = g["Games"]
            for ga in games:
                self.assertNotEqual(board_game_objects.find({"Name": ga}), None)
            publishers = g["Publishers"]
            for p in publishers:
                self.assertNotEqual(publish_objects.find({"Name": p}), None)
    def test_publishers_connect_to_other_models(self):
        for p in publish_objects.find():
            games = p["Games"]
            for g in games:
                self.assertNotEqual(board_game_objects.find({"Name": g}), None)
            genres = p["Genres"]
            for gen in genres:
                self.assertNotEqual(genre_objects.find({"Name": gen}), None)
    def test_no_game_duplicates(self):
        for b in board_game_objects.find():
            test = list(board_game_objects.aggregate([{"$match": {'Name': b["Name"]}}]))
            self.assertEqual(len(test), 1)

    def test_no_genre_duplicates(self):
        for g in genre_objects.find():
            test = list(genre_objects.aggregate([{"$match": {'Name': g["Name"]}}]))
            self.assertEqual(len(test), 1)

    def test_no_publisher_duplicates(self):
        for p in publish_objects.find():
            test = list(publish_objects.aggregate([{"$match": {'Name': p["Name"]}}]))
            self.assertEqual(len(test), 1)

if __name__ == '__main__':
    unittest.main()
