import pymongo
from pymongo import MongoClient
from mongoengine import *
# import requests


client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")

connect('BGDB', host='localhost', port=27017)

print(client.list_database_names())
print(client["BGDB"].list_collection_names())
print(client["BGDB"]["boardgamecollection"].find_one())


# resp = requests.get('https://api.boardgameatlas.com/api/search?name=Catan&client_id=zJUSH9XolY')
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for d in resp.json()['games']:
#     print (d['name'])
