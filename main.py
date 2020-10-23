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


############ ROUTES ############
game_column = db["boardgamecollection"]


@app.route('/boardgames/<string:name>')
def boardgames(name):
        query = {"Name": name}
        doc = game_column.find(query)
        publisher_link = doc["Publisher"]
        publisher_link.replace(" ", "")
        publisher_link.replace(r'[^\w]', '')
        Image_URL = doc["Image_URL"]
        return render_template('boardgames.html', doc=doc, publisher_link=publisher_link, Image_URL=Image_URL)


@app.route('/boardgamepublisher/<string:name>')
def boardgamegenres(name):
        query = {"Name": name}
        doc = game_column.find(query)
        Image_URL = doc["Image_URL"]
        return render_template('boardgames.html', doc=doc, Image_URL=Image_URL)


@app.route('/boardgamegenres/<string:name>')
def boardgamepublishers(name):
        query = {"Name": name}
        doc = game_column.find(query)

        Image_URL = doc["Image_URL"]
        return render_template('boardgames.html', doc=doc, Image_URL=Image_URL)


if __name__ == "__main__":
    app.run(debug=True)
