#This code updates all games in the games collection. If the collection is empty, it will populate it with our 123 games. 
#If this code is run while the collection already has all of our games in it, it will just update the games, and shouldn't cause any duplicates.
#If you need to clear the entire collection, see the code at the very bottom of the file.
#Let me (Allegra) know if you have any questions before you try to run this.

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

############################################FOR FIRST 100 GAMES####################################################

#API request from Board Game Atlas
resp = requests.get('https://api.boardgameatlas.com/api/search?list_id=L6t9vL6DnV&client_id=zJUSH9XolY')

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for game in resp.json()['games']:

	# you have to make a dictionary object with the info and then insert that into a collection
    newboardgame = {
    	"Name": game['name'],
    	"Category": [game['categories']],
    	"Publisher": game['publishers'][0],
    	"Description": game['description'],
    	"Min_Players": game['min_players'],
    	"Max_Players": game['max_players'],
    	"Min_Playtime": game['min_playtime'],
    	"Max_Playtime": game['max_playtime'],
    	"Year_Published": game['year_published'],
    	"Min_Age": game['min_age'],
    	"Image_URL": game['image_url'],
    	"BGA_Link": game['url']
    }

    # insert the new boardgame into the board game collection or update the existing board game by replacing the information
    boardgamecollection.replace_one({'Name': newboardgame['Name']}, newboardgame, upsert=True)

############################################FOR GAMES 101-123######################################################

#API request from Board Game Atlas
resp2 = requests.get('https://api.boardgameatlas.com/api/search?skip=100&list_id=L6t9vL6DnV&client_id=zJUSH9XolY')

if resp2.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp2.status_code))
for game in resp2.json()['games']:

    # you have to make a dictionary object with the info and then insert that into a collection
    newboardgame = {
        "Name": game['name'],
        "Category": [game['categories']],
        "Publisher": game['publishers'][0],
        "Description": game['description'],
        "Min_Players": game['min_players'],
        "Max_Players": game['max_players'],
        "Min_Playtime": game['min_playtime'],
        "Max_Playtime": game['max_playtime'],
        "Year_Published": game['year_published'],
        "Min_Age": game['min_age'],
        "Image_URL": game['image_url'],
        "BGA_Link": game['url']
    }

    # insert the new boardgame into the board game collection or update the existing board game by replacing the information
    boardgamecollection.replace_one({'Name': newboardgame['Name']}, newboardgame, upsert=True)

###########################TO UPDATE THE CATEGORIES TO ACTUAL NAMES INSTEAD OF CATEGORY IDS##################################

#API request from Board Game Atlas, to get category names
categoriesresp = requests.get('https://api.boardgameatlas.com/api/game/categories?name=Aliens&client_id=zJUSH9XolY')
categoriesfromBGA = categoriesresp.json()["categories"]
genres = {}
for cat in categoriesfromBGA:
    g= {cat['id']: cat['name']}
    genres.update(g)
print(genres)
for game in client["BGDB"]["boardgamecollection"].find():
    c = game['Category']
    genresforgame = []
    for i in c:
        for o in i:
            if o['id'] in genres:
                genresforgame.append(genres[o['id']])
    client["BGDB"]["boardgamecollection"].update_one({'Name': game['Name']}, {"$set" : {"genres": genresforgame}})


##############################################CLEAR COLLECTION###########################################################

#If for some reason you need to delete the collection entirely, comment out everything in this file besides the code below, then run.

#client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
#connect('BGDB', host='localhost', port=27017)

#db = client["BGDB"]
#boardgamecollection = db["boardgamecollection"]
#boardgamecollection.delete_many({ })

