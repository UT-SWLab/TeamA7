import pymongo
from pymongo import MongoClient
from mongoengine import *
import requests

#connects to our MongoDB server running on MongoDB Atlas
client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
connect('BGDB', host='localhost', port=27017)

#designate 'db' as the name of our database to be used in this code, and 'boardgamecollection' as the name of the collection of board games to be used in this code
db = client["BGDB"]
boardgamecollection = db["boardgamecollection"]
publishercollection = db["publishercollection"]
genrecollection = db["genrecollection"]


# for game in boardgamecollection.find():
# 	publisher = game["Publisher"]
# 	publishercollection.update_one({'Publisher': publisher}, {"$push" : {"Games": game['Name']}})

# for genre in genrecollection.find():
# 	for publisher in genre['Publishers']:
# 		publishercollection.update_one({'Publisher': publisher}, {"$push" : {"Genres": genre['Name']}})
		

# to clear the collection
# publisherscollection.delete_many({ })