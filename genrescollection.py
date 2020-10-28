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
genrecollection = db["genrecollection"]


for game in boardgamecollection.find():
	for genre in game["genres"]:
		query = {"Name": genre}
		if genrecollection.find_one(query) != None:
			genretoupdate = genrecollection.find_one(query)
			print(genretoupdate["Name"])
			genrecollection.update_one({'Name': genre}, { "$push" : {"Games": game["Name"]}})
		else:
			newgenre = {
				"Name": genre,
				"Games": [game["Name"]]
			}
			genrecollection.insert_one(newgenre)

# to clear the collection
# genrecollection.delete_many({ })