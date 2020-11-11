from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re
import FilterTesting

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
# input = string searched by user
# models = board games, genres, publishers (can be any combo of 3)
# gamefields = if looking for board games what field are we searching in (default all)
# Name, Publisher, Genre, Min_Players, etc
# genrefields = if looing for genres what fields are we searching in (default all)
# publisherfields = if looking for publishers what fields are we searching in (default all)
#, gamefields, genrefields, publisherfields add these to the left back into input variables for search when adding fields
def searchdb(input, models):
    exactmatches = {} # not case sensitive, array of all exact matches
    partialmatches = {} # not case sensitive, dict of all partial matches with key the word they're matched to
    if models['boardgames']:
        exactmatches['boardgames'] = list(boardgameobjects.find({"Name": { "$regex": "^"+input+"$", '$options': 'i'}}))
    if models['genres']:
        exactmatches['genres'] = list(genre_objects.find({"Name": { "$regex": "^"+input+"$", '$options': 'i'}}))
    if models['publishers']:
        exactmatches['publishers'] = list(publish_objects.find({"Name": { "$regex": "^"+input+"$", '$options': 'i'}}))
    partialwords = input.split()
    for word in partialwords:
        partialmatches[word] = {}
        if models['boardgames']:
            partialmatches[word]['boardgames'] = (list(boardgameobjects.find({"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}})))
        if models['genres']:
            partialmatches[word]['genres'] = (list(genre_objects.find({"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}})))
        if models['publishers']:
            partialmatches[word]['publishers'] = list(publish_objects.find({"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}}))
    return exactmatches,partialmatches
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
        return render_template('home.html', games=games, genres=genres, publishers=publishers)

@app.route('/about')
def about():
        return render_template('about.html')

############# LIST PAGES #####################


@app.route('/boardgames/<string:sort_type>/<int:page>/<string:filters>')
#
def games(page, sort_type, filters):
    global boardgameobjects
    gameobjects = boardgameobjects.find()
    filters = "nofilters"
    filteredCollection = db["testingStuff"]
    filteredCollection.drop()  # drop entire collection
    filteredCollection = db["testingStuff"]

    if filters == "year_1940_1970":
        gameobjects = FilterTesting.year_1940_1970_Filter(boardgameobjects, filteredCollection)
    #HERE BUILD filters String and just concatentat with a letter make sure to not do special character.

    if sort_type == "alphabetical":
        gameobjects = boardgameobjects.find().sort("Name")
    elif sort_type == "inverse":
        gameobjects = boardgameobjects.find().sort("Name", -1)

    #else:
    #gameobjects = boardgameobjects.find()

    max_pages = (gameobjects.collection.count()//12) + 1
    return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='/boardgames/', filters=filters)



@app.route('/boardgamegenres/<string:sort_type>/<int:page>')
def genres(page, sort_type):
    global genre_objects
    if sort_type == "alphabetical":
        genre_obj = genre_objects.find().sort("Name")
    elif sort_type == "inverse":
        genre_obj = genre_objects.find().sort("Name", -1)
    else:
        genre_obj = genre_objects.find()

    max_pages = (genre_obj.collection.count() // 12) + 1
    return render_template('Genres_List.html', genres=genre_obj, page=page, max_pages=max_pages,
                               sort_type=sort_type, page_route='/boardgamegenres/')


@app.route('/boardgamepublishers/<string:sort_type>/<int:page>')
def publishers(page, sort_type):
    global publish_objects
    if sort_type == "alphabetical":
        publish_obj = publish_objects.find().sort("Name")
    elif sort_type == "inverse":
        publish_obj = publish_objects.find().sort("Name", -1)
    else:
        publish_obj = publish_objects.find()
    max_pages = (publish_obj.collection.count() // 12) + 1
    return render_template('Publishers_List.html', publishers=publish_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='/boardgamepublishers/')

############ ROUTE TO GENRE INSTANCE PAGES ############
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

############ ROUTE TO PUBLISHER INSTANCE PAGES ############
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
    global publish_objects
    publisher = publish_objects.find({'Name': pubnamerequest}).next()
    return render_template("Publisher_Template.html", publisher=publisher, publishername=pubnamerequest)

############ ROUTE TO GAME INSTANCE PAGES ############
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
############ ROUTE TO SEARCH RESULTS ############
@app.route('/search', methods=['POST'])
def search():
    input_string = request.form['search']
    models = {'boardgames':True,'genres':True,'publishers':True}
    exactmatches, partialmatches = searchdb(input_string, models)
    return render_template("searchresults.html", input_string=input_string, exactmatches=exactmatches, partialmatches=partialmatches)
if __name__ == "__main__":
    app.run(debug=True)