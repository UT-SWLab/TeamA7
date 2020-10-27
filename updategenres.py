import pymongo
from pymongo import MongoClient
from mongoengine import *
import requests

## DO NOT RUN THIS UNLESS YOU KNOW WHAT IT DOES
## This was just a test file to manipulate the mongodb database but Sanne has added an API call that updated all
## game fields in the database to have a genres field which is an array of the genre names, rather than the
## category ids we had from BGA API from before.  It calls for the category json file and temporarily locally stores
## all the category ids to names, then updates all games in the mongodb collection

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")

connect('BGDB', host='localhost', port=27017)

#print(client.list_database_names())
#print(client["BGDB"].list_collection_names())
#print(client["BGDB"]["boardgamecollection"].find_one())
resp = requests.get('https://api.boardgameatlas.com/api/game/categories?name=Aliens&client_id=zJUSH9XolY')
categoriesfromBGA = resp.json()["categories"]
genres = {}
for cat in categoriesfromBGA:
    g= {cat['id']: cat['name']}
    genres.update(g)
    print(cat['id'])
    print(cat['name'])
print(genres)
for game in client["BGDB"]["boardgamecollection"].find():
    c = game['Category']
    print("Game Name" + game['Name'])
    genresforgame = []
    for i in c:
        for o in i:
            if o['id'] in genres:
                genresforgame.append(genres[o['id']])
    print(genresforgame)
    client["BGDB"]["boardgamecollection"].update_one({'Name': game['Name']}, {"$set" : {"genres": genresforgame}})
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for d in resp.json()['games']:
#     print (d['name'])
