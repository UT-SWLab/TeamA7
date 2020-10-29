# If you're unsure what's happening here feel free to ask me (Cedrik)
import pymongo
from pymongo import MongoClient
from mongoengine import *
import requests

# connects to our MongoDB server running on MongoDB Atlas
client = MongoClient(
    "mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
connect('BGDB', host='localhost', port=27017)

# designate 'db' as the name of our database to be used in this code, and 'boardgamecollection' as the name of the collection of board games to be used in this code
db = client["BGDB"]
boardgamecollection = db["boardgamecollection"]
genrecollection = db["genrecollection"]
publishercollection = db["publishercollection"]


listOfDicts = [{"Publisher": "Stronghold Games",
                "Description": "Founded in late 2009, the focus of Stronghold Games has been to provide maximum customer value by delivering high-quality products, and maximum customer satisfaction with Best of Breed games, i.e. games that are the finest in mechanic, theme, and/or other attributes valued by gamers.",
                },

               {"Publisher": "CMON", "Description": "This Publisher Is private and does not have public information sorry :(", },

               {"Publisher": "Hasbro", "Description": ""},

               {"Publisher": "Matagot", "Description": " "},

               {"Publisher": "Rio Grande Games", "Description": " "},

               {"Publisher": "Gozer Games, LLC", "Description": " "},

               {"Publisher": "Space Cowboys", "Description": " "},

               {"Publisher": "Jolly Roger Games", "Description": " "},

               {"Publisher": "Playroom Entertainment", "Description": " "},

               {"Publisher": "Gamewright", "Description": " "},

               {"Publisher": "Darktier Studios", "Description": " "},

               {"Publisher": "Asmodee", "Description": " "},
               {"Publisher": "PD-Verlag", "Description": " "},

               {"Publisher": "Secret Hitler", "Description": " "},

               {"Publisher": "IELLO", "Description": " "},

               {"Publisher": "Fantasy Flight Games", "Description": " "},

               {"Publisher": "Brain Games", "Description": " "},

               {"Publisher": "TwinbroGames", "Description": " "},

               {"Publisher": "Serious Poulp", "Description": " "},

               {"Publisher": "Die-Hard Games LLC", "Description": " "},

               {"Publisher": "Gamelyn Games", "Description": " "},

               {"Publisher": "Grail Games", "Description": " "},

               {"Publisher": "Wizards of the Coast", "Description": " "},

               {"Publisher": "Avalon Hill Games  Inc.", "Description": " "},

               {"Publisher": "R&D Games", "Description": " "},

               {"Publisher": "Game Salute", "Description": " "},

               {"Publisher": "KOSMOS", "Description": " "},

               {"Publisher": "NSKN Games", "Description": " "},

               {"Publisher": "Bézier Games", "Description": " "},

               {"Publisher": "Splotter Spellen", "Description": " "},

               {"Publisher": "Czech Games Edition", "Description": " "},
               {"Publisher": "Gen42 Games", "Description": " "},

               {"Publisher": "Indie Boards & Cards", "Description": " "},

               {"Publisher": "Renegade Game Studios", "Description": " "},

               {"Publisher": "Arcane Wonders", "Description": " "},

               {"Publisher": "Plan B Games", "Description": " "},

               {"Publisher": "Asmodee Editions", "Description": " "},

               {"Publisher": "Lookout Games", "Description": " "},

               {"Publisher": "Grey Fox Games", "Description": " "},

               {"Publisher": "Alderac Entertainment Group", "Description": " "},

               {"Publisher": "Pandasaurus Games", "Description": " "},

               {"Publisher": "WizKids", "Description": " "},

               {"Publisher": "Ceaco", "Description": " "},

               {"Publisher": "GMT Games", "Description": " "},

               {"Publisher": "Z-Man Games  Inc.", "Description": " "},

               {"Publisher": "Libellud", "Description": " "},

               {"Publisher": "ABACUSSPIELE", "Description": " "},

               {"Publisher": "Portal Games", "Description": " "},

               {"Publisher": "Thames & Kosmos", "Description": " "},

               {"Publisher": "Days of Wonder", "Description": " "},

               {"Publisher": "Garphill Games", "Description": " "},

               {"Publisher": "Tasty Minstrel Games", "Description": " "},

               {"Publisher": "Floodgate Games", "Description": " "},

               {"Publisher": "Plaid Hat Games", "Description": " "},
               {"Publisher": "North Star Games", "Description": " "},

               {"Publisher": "Blue Cocker", "Description": " "},

               {"Publisher": "Karma Games", "Description": " "},

               {"Publisher": "White Wizard Games", "Description": " "},

               {"Publisher": "Z-Man Games", "Description": " "},

               {"Publisher": "Blue Orange Games", "Description": " "},

               {"Publisher": "eggertspiele", "Description": " "},

               {"Publisher": "Spin Master", "Description": " "},

               {"Publisher": "Roxley", "Description": " "},

               {"Publisher": "Ravensburger", "Description": " "},

               {"Publisher": "Hans im Glück", "Description": " "},

               {"Publisher": "Repos Production", "Description": " "},

               {"Publisher": "Greater Than Games", "Description": " "},

               {"Publisher": "Next Move Games", "Description": " "},

               {"Publisher": "Stonemaier Games", "Description": " "},

               {"Publisher": "Leder Games", "Description": " "},

               {"Publisher": "Cephalofair Games", "Description": " "}]

for i in range(len(listOfDicts)):
    Dict = listOfDicts[i]
    publishercollection.insert_one(Dict)

#publishercollection.delete_many({})

'''
publishercollection.insert_all(publisherSuperDict)

# to clear the collection

# publishercollection.delete_many({})
'''
