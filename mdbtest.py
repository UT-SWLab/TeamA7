import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
from classes import BoardGame, Publisher, Category


client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]

connect('BGDB', host='localhost', port=27017)


# resp = requests.get('https://api.boardgameatlas.com/api/search?list_id=LXkpj3Jto9&client_id=zJUSH9XolY')
# if resp.status_code != 200:
    # This means something went wrong.
    # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for game in resp.json()['games']:
#     newBoardGame = BoardGame(name=game['name'])
#     newBoardGame.categories = game['categories']
#     newBoardGame.publisher = game['primary_publisher']
#     newBoardGame.description = game['description']
#     newBoardGame.min_players = game['min_players']
#     newBoardGame.max_players = game['max_players']
#     newBoardGame.min_playtime = game['min_playtime']
#     newBoardGame.max_playtime = game['max_playtime']
#     newBoardGame.year_published = game['year_published']
#     newBoardGame.min_age = game['min_age']
#     newBoardGame.image_url = game['image_url']
#     newBoardGame.website = game['official_url']
#     #add board game to database
#     newBoardGame.save()

for game in BoardGame.objects:
    print(game['name'])




