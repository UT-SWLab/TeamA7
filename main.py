from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re

client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
boardgameobjects = client["BGDB"].boardgamecollection
gamepagerequest = ''
pubnamerequest = ''
genre_name_request = ''
pubpagerequest = {}
genre_page_request = {}
app = Flask(__name__)
def GameLinkify(name):
    linkformat = re.compile('[^a-zA-Z0-9]')
    linkname = linkformat.sub('', name)
    return linkname
def PublisherNames():
    bgc = boardgameobjects.find()
    publishernames = []
    for game in bgc:
        if game['Publisher'] not in publishernames:
            publishernames.append(game['Publisher'])
    return(publishernames)


@app.route('/')
def home():
        return render_template('home.html')


@app.route('/about')
def about():
        return render_template('about.html')

### LIST PAGES ###


@app.route('/boardgames/<int:page>')
def games(page):
        global boardgameobjects
        gameobjects = boardgameobjects.find()
        return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page,)


@app.route('/boardgamegenres', methods=['POST', 'GET'])
def genres():
        return render_template('Genres_Template.html')


@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
    global boardgameobjects
    publishers = PublisherNames()
    return render_template('Publishers_List.html', publishernames=publishers, gameobjects=boardgameobjects)

############ ROUTE TO PUBLISHERS SB ############


@app.route('/genre', methods=['POST'])
def genre_routing():
    genre_name = request.form['genrename']
    global genre_name_request
    genre_name_request = genre_name
    genre_link = GameLinkify(genre_name)
    global genre_page_request
    genre_page_request = boardgameobjects.find({'genres': genre_name})
    return redirect(url_for('.genre_page', genre_link=genre_link))


@app.route('/genre/<genre_link>', methods=['POST', 'GET'])
def genre_page(genre_link):
    return render_template("Genre_Template.html", genre_games=genre_page_request)


@app.route('/publisher', methods=['POST'])
def PubRouting():
    publishername = request.form['publishername']
    global pubnamerequest
    pubnamerequest = publishername
    publisherlink = GameLinkify(publishername)
    global pubpagerequest
    pubpagerequest = boardgameobjects.find({'Publisher': publishername})
    return redirect(url_for('.PubPage', publisherlink=publisherlink))


@app.route('/publisher/<publisherlink>', methods=['POST', 'GET'])
def PubPage(publisherlink):
    return render_template("Publisher_Template.html", gamesforpub=pubpagerequest, publishername=pubnamerequest)

############ ROUTE TO GAMES SB ############


@app.route('/game', methods=['POST'])
def GameRouting():
    gamename = request.form['gamename']
    gamelink = GameLinkify(gamename)
    global gamepagerequest
    gamepagerequest = gamename
    return redirect(url_for('.GamePage', gamelink=gamelink))


@app.route('/<gamelink>')
def GamePage(gamelink):
    global gamepagerequest
    game = boardgameobjects.find({'Name': gamepagerequest}).next()
    return render_template("Board_Game_Template.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)


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