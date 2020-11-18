from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re
import FilterTesting

client = MongoClient(
    "mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
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

saveSort = 'normal'

LiveFilters = []

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
# , gamefields, genrefields, publisherfields add these to the left back into input variables for search when adding fields
def searchdb(input, models):
    exactmatches = {}  # not case sensitive, array of all exact matches
    partialmatches = {}  # not case sensitive, dict of all partial matches with key the word they're matched to
    if models['boardgames']:
        matches = list(boardgameobjects.find({"$or": [
            {"Name": {"$regex": ".*" + input + ".*", '$options': 'i'}},  # game name matches
            {"Description": {"$regex": ".*" + input + ".*", '$options': 'i'}},  # game description matches
            {"Publisher": {"$regex": ".*" + input + ".*", '$options': 'i'}},  # game publisher matches
            {"genres": {"$regex": ".*" + input + ".*", '$options': 'i'}}  # game genres matches
        ]}))

        exactmatches['boardgames'] = matches
    if models['genres']:
        matches = list(genre_objects.find({"$or": [
            {"Name": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Description": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Publishers": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Games": {"$regex": ".*" + input + ".*", '$options': 'i'}}
        ]}))
        exactmatches['genres'] = matches
    if models['publishers']:
        matches = list(publish_objects.find({"$or": [
            {"Name": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Description": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Genres": {"$regex": ".*" + input + ".*", '$options': 'i'}},
            {"Games": {"$regex": ".*" + input + ".*", '$options': 'i'}}
        ]}))
        exactmatches['publishers'] = matches
    partialwords = input.split()
    if len(partialwords) > 1:
        for word in partialwords:
            partialmatches[word] = {}
            if models['boardgames']:
                final = []
                matches = list(boardgameobjects.find({"$or": [
                    {"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Description": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Publisher": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"genres": {"$regex": ".*" + word + ".*", '$options': 'i'}}
                ]}))
                for m in matches:
                    if m not in exactmatches['boardgames']:
                        final.append(m)
                partialmatches[word]['boardgames'] = final
            if models['genres']:
                final = []
                matches = list(genre_objects.find({"$or": [
                    {"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Description": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Games": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Publishers": {"$regex": ".*" + word + ".*", '$options': 'i'}}
                ]}))
                for m in matches:
                    if m not in exactmatches['genres']:
                        final.append(m)
                partialmatches[word]['genres'] = final
            if models['publishers']:
                final = []
                matches = list(publish_objects.find({"$or": [
                    {"Name": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Description": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Genres": {"$regex": ".*" + word + ".*", '$options': 'i'}},
                    {"Games": {"$regex": ".*" + word + ".*", '$options': 'i'}}
                ]}))
                for m in matches:
                    if m not in exactmatches['publishers']:
                        final.append(m)
                partialmatches[word]['publishers'] = final
    return exactmatches, partialmatches


def PublisherNames():
    # Function now returns tupple of list to so game and publisher are tied for publisher page elements.
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
    # print (publishernames) #Debuggin
    # print (publishernameGame)
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
def games(page, sort_type, filters):
    global boardgameobjects

    filteredCollection = CheckSubstringMatches(filters, boardgameobjects)

    # Apply ordering to filtered collection.
    if sort_type == "alphabetical":
        gameobjects = filteredCollection.find().sort("Name")

    elif sort_type == "inverse":
        gameobjects = filteredCollection.find().sort("Name", -1)

    else:
        # Case where no sorting is done, Give Cursor to list_Base Page
        gameobjects = filteredCollection.find()

    max_pages = ((gameobjects.collection.count() - 1) // 12) + 1
    return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgames', filters=filters)


@app.route('/boardgamegenres/<string:sort_type>/<int:page>/<string:filters>')
def genres(page, sort_type, filters):
    global genre_objects

    filteredCollection = CheckSubstringMatches(filters, genre_objects)

    if sort_type == "alphabetical":
        genre_obj = filteredCollection.find().sort("Name")
    elif sort_type == "inverse":
        genre_obj = filteredCollection.find().sort("Name", -1)
    else:
        genre_obj = filteredCollection.find()

    max_pages = ((genre_obj.collection.count() - 1) // 12) + 1
    return render_template('Genres_List.html', genres=genre_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamegenres', filters=filters)


@app.route('/boardgamepublishers/<string:sort_type>/<int:page>/<string:filters>')
def publishers(page, sort_type, filters):
    global publish_objects

    filteredCollection = CheckSubstringMatches(filters, publish_objects)


    if sort_type == "alphabetical":
        publish_obj = filteredCollection.find().sort("Name")
    elif sort_type == "inverse":
        publish_obj = filteredCollection.find().sort("Name", -1)
    else:
        publish_obj = filteredCollection.find()
    max_pages = ((publish_obj.collection.count() - 1) // 12) + 1
    return render_template('Publishers_List.html', publishers=publish_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamepublishers', filters=filters)


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
    type = ''
    models = {'boardgames': False, 'genres': False, 'publishers': False}
    if "modeltype" in request.form:
        type = request.form["modeltype"]
        models[type] = True;
        if type == "all":
            models = {'boardgames': True, 'genres': True, 'publishers': True}
    exactmatches, partialmatches = searchdb(input_string, models)
    return render_template("searchresults.html", input_string=input_string, exactmatches=exactmatches,
                           partialmatches=partialmatches, modeltype=type)


####################FILTERS#####################

def noFilter(cur, filteredCollection):
    for match in cur.find():
        filteredCollection.insert_one(match)
    return filteredCollection


def two_to_four_players_Filter(filteredCollection):
    num = 4
    smallerCollection = db["smallerCollection"]
    smallerCollection.drop()
    smallerCollection = db["smallerCollection"]
    for match in filteredCollection.find({"Min_Players": {"$lt": num}}):
        smallerCollection.insert_one(match)
    return smallerCollection


def CheckSubstringMatches(filters, NonFilteredCollection):
    Allfilters = ['four_or_more_players', 'two_to_four_players', 'less_than_2hrs', 'year_1940_1970', 'less_than_1hrs',
                  'half_hour_or_less']
    fullstring = filters
    FoundFilters = list()

    dictYear1940_1970 = {"Year_Published": {"$gt": 1939, "$lt": 1971}}
    dicthalf_hour_or_less = {"Max_Playtime": {"$lte": 30}}
    dictfour_or_more_players = {"Min_Players": {"$gt": 3}}

    dictless_than_1hrs = {"Max_Playtime": {"$lt": 61}}
    dictless_than_2hrs = {"Max_Playtime": {"$lt": 121}}
    dicttwo_to_four_players = {"Min_Players": {"$eq": 2}, "Max_Players": {"$eq": 4}}

    for specificFilter in Allfilters:
        substring = specificFilter
        if fullstring.find(substring) != -1:
            print("Found: " + substring)
            FoundFilters.append(substring)

        else:
            print(substring + ": Not found")
    listofFindCommands = []

    for filter in FoundFilters:
        if filter == 'year_1940_1970':
            listofFindCommands.append(dictYear1940_1970)
        if (filter == 'half_hour_or_less'):
            listofFindCommands.append(dicthalf_hour_or_less)
        if (filter == 'less_than_2hrs'):
            listofFindCommands.append(dictless_than_2hrs)
        if (filter == 'two_to_four_players'):
            listofFindCommands.append(dicttwo_to_four_players)
        if (filter == 'less_than_1hrs'):
            listofFindCommands.append(dictless_than_1hrs)
        if (filter == 'four_or_more_players'):
            listofFindCommands.append(dictfour_or_more_players)

    basedictionary = {"$and": listofFindCommands}
    return ApplyFoundFilters(FoundFilters, NonFilteredCollection,
                             basedictionary)  # This function returns filtered collection


def ApplyFoundFilters(FoundFliters, NonFilteredCollection, basedictionary):
    # NonFilteredCollection is boardgame collections. This is used as a super collection.
    filteredCollection = db["FinalFiltered"]
    filteredCollection.drop()  # drop entire collection
    filteredCollection = db["FinalFiltered"]

    if len(FoundFliters) == 0:
        # if no filters then just leave.
        return NonFilteredCollection
    # .find({"$and": [filters]})
    cur = NonFilteredCollection.find(basedictionary)
    for element in cur:
        filteredCollection.insert_one(element)

    '''
    for filter in FoundFliters:
        if filter == 'year_1940_1970':
            filteredCollection = year_1940_1970_Filter(filteredCollection)

        if filter == 'less_than_1hrs':
            filteredCollection = less_than_1hrs_Filter (filteredCollection)

        if (filter == 'less_than_2hrs'):
            filteredCollection = less_than_2hrs_Filter(filteredCollection)
        if (filter == 'two_to_four_players'):
            filteredCollection = two_to_four_players_Filter(filteredCollection)

        if (filter == 'four_or_more_players'):
            filteredCollection = four_or_more_players_Filter(filteredCollection)

        if (filter == 'half_hour_or_less'):
            print("hit half hour")
            filteredCollection = half_hour_or_less_Filter(filteredCollection)
    '''

    return filteredCollection  # This collection should be totally filtered


if __name__ == "__main__":
    app.run(debug=True)
