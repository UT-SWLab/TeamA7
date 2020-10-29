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
genre_objects = client["BGDB"].genrecollection
publish_objects = client["BGDB"].publishercollection
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
    #Function now returns tupple of list to so game and publisher are tied for publisher page elements.
    bgc = boardgameobjects.find()
    publishernames = []
    publishernameGame = []
    publishYear = []
    for game in bgc:
        if game['Publisher'] not in publishernames:
            if game['Publisher'] == 'None':
                game['Publisher'] = "unaffiliated"
            publishernames.append(game['Publisher'])
            publishernameGame.append(game['Name'])
            publishYear.append(game['Year_Published'])
    #print (publishernames) #Debuggin
    #print (publishernameGame)
    return publishernames, publishernameGame, publishYear




@app.route('/')
def home():
        games = boardgameobjects.find().limit(3)
        genres = genre_objects.find().limit(3)
        publishers = publish_objects.find().limit(3)
        pubimages = ['', '', '']
        for p in range(0,3):
            g = boardgameobjects.find({"Publisher": publishers[p]['Publisher']}).next()
            pubimages[p] = g['Image_URL']
        return render_template('home.html', games=games, genres=genres, publishers=publishers, pubimages=pubimages)


@app.route('/about')
def about():
        return render_template('about.html')

### LIST PAGES ###


@app.route('/boardgames/<int:page>')
def games(page):
        global boardgameobjects
        gameobjects = boardgameobjects.find()
        return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page,)


@app.route('/boardgamegenres/<int:page>')
def genres(page):
        global genre_objects
        genre_obj = genre_objects.find()
        return render_template('Genres_List.html', genres=genre_obj, page=page)


@app.route('/boardgamepublishers/<int:page>', methods=['POST', 'GET'])
def publishers(page):
    global boardgameobjects
    publishersTupple = PublisherNames()
    publishers = publishersTupple[0]
    publishergame = publishersTupple[1]
    publishyear = publishersTupple[2]
    gameobjects = boardgameobjects.find()
    return render_template('Publishers_List.html',  publishernames=publishers, gameobjects=gameobjects, publishergame=publishergame, publishyear=publishyear, page=page)

############ ROUTE TO PUBLISHERS SB ############


@app.route('/genre', methods=['POST'])
def genre_routing():
    genre_name = request.form['genrename']
    global genre_name_request
    genre_name_request = genre_name
    genre_link = GameLinkify(genre_name)
    return redirect(url_for('.genre_page', genre_link=genre_link))


@app.route('/genre/<genre_link>', methods=['POST', 'GET'])
def genre_page(genre_link):
    global genre_name_request
    global genre_objects
    genre = genre_objects.find({'Name': genre_name_request}).next()
    return render_template("Genre_Template.html", genre=genre)


@app.route('/publisher', methods=['POST'])
def PubRouting():
    publisher_name = request.form['publishername']
    global pubnamerequest
    pubnamerequest = publisher_name
    publisherlink = GameLinkify(publisher_name)
    return redirect(url_for('.PubPage', publisherlink=publisherlink))


@app.route('/publisher/<publisherlink>', methods=['POST', 'GET'])
def PubPage(publisherlink):
    global pubnamerequest
    publisher = publish_objects.find({'Publisher': pubnamerequest}).next()
    publishersTupple = PublisherNames()
    publishers = publishersTupple[0]
    publishergame = publishersTupple[1]
    publishyear = publishersTupple[2]
    return render_template("Publisher_Template.html", publisher=publisher, gamesforpub=publishergame, publishername=pubnamerequest, publishyear=publishyear)


############ ROUTE TO GAMES SB ############


@app.route('/game', methods=['POST'])
def GameRouting():
    gamename = request.form['gamename']
    gamelink = GameLinkify(gamename)
    global gamepagerequest
    gamepagerequest = gamename
    return redirect(url_for('.GamePage', gamelink=gamelink))


@app.route('/game/<gamelink>')
def GamePage(gamelink):
    global gamepagerequest
    game = boardgameobjects.find({'Name': gamepagerequest}).next()
    return render_template("Board_Game_Template.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)


# game_column = db["boardgamecollection"]
#
#
# @app.route('/boardgames/<string:name>')
# def boardgames(name):
#         query = {"Name": name}
#         doc = game_column.find(query)
#         publisher_link = doc["Publisher"]
#         publisher_link.replace(" ", "")
#         publisher_link.replace(r'[^\w]', '')
#         Image_URL = doc["Image_URL"]
#         return render_template('boardgames.html', doc=doc, publisher_link=publisher_link, Image_URL=Image_URL)
#
#
# @app.route('/boardgamepublisher/<string:name>')
# def boardgamegenres(name):
#         query = {"Name": name}
#         doc = game_column.find(query)
#         Image_URL = doc["Image_URL"]
#         return render_template('boardgames.html', doc=doc, Image_URL=Image_URL)
#
#
# @app.route('/boardgamegenres/<string:name>')
# def boardgamepublishers(name):
#     query = {"Name": name}
#     doc = game_column.find(query)
#     Image_URL = doc["Image_URL"]
#     return render_template('boardgames.html', doc=doc, Image_URL=Image_URL)