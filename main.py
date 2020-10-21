from flask import Flask, render_template, url_for, request, redirect
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]

connect('BGDB', host='localhost', port=27017)

app = Flask(__name__)


@app.route('/')
def home():
        return render_template('home.html')


@app.route('/about')
def about():
        return render_template('about.html')


@app.route('/boardgames')
def games():
        return render_template('Board_Games_List.html')


@app.route('/boardgamegenres')
def genres():
        return render_template('Genres_List.html')

@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
        return render_template('Publishers_List.html')


############ ROUTES TO PUBLISHERS ############
game_column = db["boardgamecollection"]


@app.route('/boardgames/<string:name>')
def boardgames(name):
        query = {"Name": name}
        doc = game_column.find(query)
        publisher_link = doc["Publisher"]
        Image_URL = doc["Image_URL"]
        return render_template('boardgames.html', doc=doc, publisher_link=publisher_link, Image_URL=Image_URL)


@app.route('/RioGrandeGames', methods=['POST', 'GET'])
def RioGrandeGames():
        return render_template('RioGrandeGames.html')

@app.route('/Mattel', methods=['POST', 'GET'])
def Mattel():
        return render_template('Mattel.html')

@app.route('/Hasbro', methods=['POST', 'GET'])
def Hasbro():
        return render_template('Hasbro.html')


############ ROUTES TO GAMES ############

@app.route('/ApplestoApples', methods=['POST', 'GET'])
def ApplestoApples():
        return render_template('Board_Game_Template.html')


@app.route('/Dominion', methods=['POST', 'GET'])
def Dominion():
        return render_template('Dominion.html')

@app.route('/Scrabble', methods=['POST', 'GET'])
def Scrabble():
        return render_template('Scrabble.html')


############ ROUTES TO GENRES ############
@app.route('/boardgamegenres/<string:name>')
def genres(name):

        return render_template('genres.html')


@app.route('/DeckBuilders', methods=['POST', 'GET'])
def DeckBuilders():
        return render_template('DeckBuilders.html')


@app.route('/PartyGames', methods=['POST', 'GET'])
def PartyGames():
        return render_template('PartyGames.html')

@app.route('/WordGames', methods=['POST', 'GET'])
def WordGames():
        return render_template('WordGames.html')


if __name__ == "__main__":
    app.run(debug=True)
