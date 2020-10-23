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
pubnamerequest= ''
pubpagerequest = {}
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

@app.route('/boardgames')
def games():
        global boardgameobjects
        gameobjects=boardgameobjects.find()
        return render_template('Board_Games_List.html', gameobjects=gameobjects)

@app.route('/boardgamegenres', methods=['POST', 'GET'])
def genres():
        return render_template('Genres_List.html')

@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
    global boardgameobjects
    publishers = PublisherNames()
    return render_template('Publishers_List.html', publishernames=publishers, gameobjects=boardgameobjects)


############ ROUTES TO PUBLISHERS ############
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

############ ROUTES TO GAMES ############
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

############ ROUTES TO GENRES ############

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
