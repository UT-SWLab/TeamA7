#you may need to download some of these things to get this code (or similar code) to work
#let me (Allegra) know if you have any questions
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

#API request from Board Game Atlas
#for first 100 games
# resp = requests.get('https://api.boardgameatlas.com/api/search?list_id=L6t9vL6DnV&client_id=zJUSH9XolY')
#for games after 100
# resp = requests.get('https://api.boardgameatlas.com/api/search?skip=100&list_id=L6t9vL6DnV&client_id=zJUSH9XolY')
# if resp.status_code != 200:
    # This means something went wrong.
    # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for game in resp.json()['games']:
	#this is what's most important for inserting things into the database
	#you have to make a dictionary object with the info and then insert that into a collection
    # newboardgame = {
    # 	"Name": game['name'],
    # 	"Category": [game['categories']],
    # 	"Publisher": game['primary_publisher'],
    # 	"Description": game['description'],
    # 	"Min_Players": game['min_players'],
    # 	"Max_Players": game['max_players'],
    # 	"Min_Playtime": game['min_playtime'],
    # 	"Max_Playtime": game['max_playtime'],
    # 	"Year_Published": game['year_published'],
    # 	"Min_Age": game['min_age'],
    # 	"Image_URL": game['image_url'],
    # 	"BGA_Link": game['url']
    # }


    # insert the new boardgame dictionary into the board game collection
    # boardgamecollection.insert_one(newboardgame)


#to clear the collection
#boardgamecollection.delete_many({ })

