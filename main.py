from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re

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
# models = board games, genres, publishers
# fields = array of strings of fields searched in each model (default is all fields)
def searchdb(input, models, fields):
    exactmatches = {}  # not case sensitive, array of all exact matches
    partialmatches = {}  # not case sensitive, dict of all partial matches with key the word they're matched to
    partialwords = list(input.split())
    if len(partialwords) == 1:
        partialwords = []
    if models['boardgames']:
        game_fields = fields
        if list(fields) == ["all"]:
            game_fields = ["Name", "Description", "Publisher", "genres"]
        exact_search = []
        for f in game_fields:
            exact_search.append({f: {"$regex": ".*" + input + ".*", '$options': 'i'}})
        exactmatches['boardgames'] = list(boardgameobjects.find({"$or": exact_search}))
        for w in partialwords:
            if w not in partialmatches:
                partialmatches[w] = {}
            fieldsearches = []
            for f in game_fields:
                fieldsearches.append({f: {"$regex": ".*" + w + ".*", '$options': 'i'}})
            partialmatches[w]['boardgames'] = list(filter(lambda g: g not in exactmatches['boardgames'],
                                                          (list(boardgameobjects.find({"$or": fieldsearches})))))
    if models['genres']:
        genre_fields = fields
        if list(fields) == ["all"]:
            genre_fields = ["Name", "Description", "Publishers", "Games"]
        exact_search = []
        for f in genre_fields:
            if f == "Publisher":
                exact_search.append({"Publishers": {"$regex": ".*" + input + ".*", '$options': 'i'}})
            else:
                exact_search.append({f: {"$regex": ".*" + input + ".*", '$options': 'i'}})
        exactmatches['genres'] = list(genre_objects.find({"$or": exact_search}))
        for w in partialwords:
            if w not in partialmatches:
                partialmatches[w] = {}
            fieldsearches = []
            for f in genre_fields:
                fieldsearches.append({f: {"$regex": ".*" + w + ".*", '$options': 'i'}})
            partialmatches[w]['genres'] = list(filter(lambda g: g not in exactmatches['genres'],
                                                      (list(genre_objects.find({"$or": fieldsearches})))))
    if models['publishers']:
        publisher_fields = fields
        if list(fields) == ["all"]:
            publisher_fields = ["Name", "Description", "Genres", "Games"]
        exact_search = []
        for f in publisher_fields:
            if f == "genres":
                exact_search.append({"Genres": {"$regex": ".*" + input + ".*", '$options': 'i'}})
            else:
                exact_search.append({f: {"$regex": ".*" + input + ".*", '$options': 'i'}})
        exactmatches['publishers'] = list(publish_objects.find({"$or": exact_search}))
        for w in partialwords:
            if w not in partialmatches:
                partialmatches[w] = {}
            fieldsearches = []
            for f in publisher_fields:
                fieldsearches.append({f: {"$regex": ".*" + w + ".*", '$options': 'i'}})
            partialmatches[w]['publishers'] = list(filter(lambda g: g not in exactmatches['publishers'],
                                                          (list(publish_objects.find({"$or": fieldsearches})))))
    return exactmatches, partialmatches


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

    elif sort_type == "min-playtime":
        gameobjects = filteredCollection.find().sort("Min_Playtime")

    elif sort_type == "min-players":
        gameobjects = filteredCollection.find().sort("Min_Players")

    else:
        # Case where no sorting is done, Give Cursor to list_Base Page
        gameobjects = filteredCollection.find()
    empty = filteredCollection.count() == 0
    max_pages = ((gameobjects.collection.count() - 1) // 12) + 1
    return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgames', filters=filters, empty=empty)


@app.route('/boardgamegenres/<string:sort_type>/<int:page>/<string:filters>')
def genres(page, sort_type, filters):
    global genre_objects

    filteredCollection = CheckSubstringMatches(filters, genre_objects)

    if sort_type == "alphabetical":
        genre_obj = filteredCollection.find().sort("Name")
    elif sort_type == "inverse":
        genre_obj = filteredCollection.find().sort("Name", -1)

    elif sort_type == "min-playtime":
        genre_obj = filteredCollection.find().sort("Average_Min_Playtime")

    elif sort_type == "min-players":
        genre_obj = filteredCollection.find().sort("Average_Min_Players")
    else:
        genre_obj = filteredCollection.find()
    empty = filteredCollection.count() == 0
    max_pages = ((genre_obj.collection.count() - 1) // 12) + 1
    return render_template('Genres_List.html', genres=genre_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamegenres', filters=filters, empty=empty)


@app.route('/boardgamepublishers/<string:sort_type>/<int:page>/<string:filters>')
def publishers(page, sort_type, filters):
    global publish_objects

    filteredCollection = CheckSubstringMatches(filters, publish_objects)

    if sort_type == "alphabetical":
        publish_obj = filteredCollection.find().sort("Name")
    elif sort_type == "inverse":
        publish_obj = filteredCollection.find().sort("Name", -1)

    elif sort_type == "min-playtime":
        publish_obj = filteredCollection.find().sort("Average_Min_Playtime")

    elif sort_type == "min-players":
        publish_obj = filteredCollection.find().sort("Average_Min_Players")

    else:
        publish_obj = filteredCollection.find()

    empty = filteredCollection.count() == 0
    max_pages = ((publish_obj.collection.count() - 1) // 12) + 1
    return render_template('Publishers_List.html', publishers=publish_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamepublishers', filters=filters,
                           empty=empty)


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
    return render_template("Genre_Template.html", genre=genre, boardgames=boardgameobjects)


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
    return render_template("Publisher_Template.html", publisher=publisher, boardgames=boardgameobjects)


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
    return render_template("Board_Game_Template.html", game=game, model=game)


############ ROUTE TO SEARCH RESULTS ############
@app.route('/search', methods=['POST'])
def search():
    input_string = request.form['search']
    type = request.form["modeltype"]
    models = {'boardgames': False, 'genres': False, 'publishers': False}
    fields = ['all']
    if type == "all":
        models = {'boardgames': True, 'genres': True, 'publishers': True}
    else:
        models[type] = True;
    if "fields" in request.form:
        fromform = request.form["fields"]
        if fromform != "all":
            fields = fromform.split()
    exactmatches, partialmatches = searchdb(input=input_string, models=models, fields=fields)
    return render_template("searchresults.html", input_string=input_string, exactmatches=exactmatches,
                           partialmatches=partialmatches, modeltype=type)


####################FILTERS#####################

def noFilter(cur, filteredCollection):
    for match in cur.find():
        filteredCollection.insert_one(match)
    return filteredCollection


'''
        '1_Hour_or_More',
        '1_Hour_or_Less',
        '30_Minutes_or_Less',

        'Players:_2',
        'Players:_3',
        'Players:_4',
        'Players:_5 +',

        'Average_Price:_$30_or_More',
        'Average_Price:_$30_or_Less',
        'Average_Price:_$15_or_Less',

        'Average_Playtime:_30_minutes_or_Less',
        'Average_Playtime:_1_Hour_or_Less',
        'Average_Playtime:_1_Hour_or_More',
        'Average_Playtime:_30_Minutes_or_More',

        'Average_Price:_$30_or_More_Publisher',
        'Average_Price:_$30_or_Less_Publisher',
        'Average_Price:_$15_or_Less_Publisher',
        'Average_Price:_$30_or_More_Double'

'''


def CheckSubstringMatches(filter, NonFilteredCollection):
    if filter == "nofilters":
        return NonFilteredCollection

    listofFindCommands = []
    if (filter.split('_')[1]) == 'Hour':
        Minutes = int(filter.split('_')[0]) * 60
        if (filter.split('_')[3]) == 'More':
            listofFindCommands.append({"Max_Playtime": {"$gte": Minutes}})
        else:
            listofFindCommands.append({"Max_Playtime": {"$lte": Minutes}})

    if (filter.split('_')[1]) == 'Minutes':
        listofFindCommands.append({"Max_Playtime": {"$lte": int(filter.split('_')[0])}})

    # Need to multiply by 60.
    # dict_1_Hour_or_More = {"Max_Playtime": {"$gte": 60}}
    # dict_1_Hour_or_Less = {"Max_Playtime": {"$lte": 60}}
    ###################################################
    # dict_30_Minutes_or_Less = {"Max_Playtime": {"$lte": 30}}
    ###################################################

    if (filter.split('_')[0]) == 'Players:':
        numberOfPlayers = int((filter.split('_')[1]).strip('+'))  # Necessary for 5 + case
        listofFindCommands.append({"$and": [{"Min_Players": {"$lte": numberOfPlayers}},
                                            {"Max_Players": {"$gte": numberOfPlayers}}]})

    # dict_Players_2 = {"$and": [{"Min_Players": {"$lte": 2}}, {"Max_Players": {"$gte": 2}}]}
    # dict_Players_3 = {"$and": [{"Min_Players": {"$lte": 3}}, {"Max_Players": {"$gte": 3}}]}
    # dict_Players_4 = {"$and": [{"Min_Players": {"$lte": 4}}, {"Max_Players": {"$gte": 4}}]}
    # dict_Players_5 = {"$and": [{"Min_Players": {"$lte": 5}}, {"Max_Players": {"$gte": 5}}]}
    ###################################################
    dict_Average_Price_30_or_More = {"Average_Price_Float": {"$gte": 30}}
    dict_Average_Price_30_or_Less = {"Average_Price_Float": {"$lte": 30}}
    dict_Average_Price_15_or_Less = {"Average_Price_Float": {"$lte": 15}}
    ###################################################
    print("This is the filter " + filter)
    if (filter.split('_')[0]) == 'Average':
        print("Inside Fucn")
        Price =   int (filter.split('_')[2].strip('$'))
        print("This is the Price " + str(Price))
        if (filter.split('_')[4]) == 'More':
            listofFindCommands.append({"Average_Price_Float": {"$gte": Price}})
        if (filter.split('_')[4]) == 'Less':
            listofFindCommands.append({"Average_Price_Float": {"$lte": Price}})

    ###################################################
    dict_Average_Playtime_1_Hour_or_More = {"Average_Playtime": {"$gte": 60}}
    dict_Average_Playtime_30_Minutes_or_More = {"Average_Playtime": {"$gte": 30}}
    ###################################################
    dict_Average_Playtime_1_Hour_or_Less = {"Average_Playtime": {"$lte": 60}}
    dict_Average_Playtime_30_minutes_or_Less = {"Average_Playtime": {"$lte": 30}}

    ###########GAME CALLS TO DATABASE###################
    # if (filter == '1_Hour_or_More'):
    #    listofFindCommands.append(dict_1_Hour_or_More)
    # if (filter == '1_Hour_or_Less'):
    #   listofFindCommands.append(dict_1_Hour_or_Less)
    # if (filter == '30_Minutes_or_Less'):
    #   listofFindCommands.append(dict_30_Minutes_or_Less)
    # if (filter == 'Players:_2'):
    #   listofFindCommands.append(dict_Players_2)
    # if (filter == 'Players:_3'):
    #   listofFindCommands.append(dict_Players_3)
    # if (filter == 'Players:_4'):
    #   listofFindCommands.append(dict_Players_4)
    # if (filter == 'Players:_5 +'):
    #   listofFindCommands.append(dict_Players_5)
    ###########GENRES CALLS TO DATABASE#################
    # if (filter == 'Average_Price:_$30_or_More'):
    #    listofFindCommands.append(dict_Average_Price_30_or_More)
    # if (filter == 'Average_Price:_$30_or_Less'):
    #   listofFindCommands.append(dict_Average_Price_30_or_Less)
    # if (filter == 'Average_Price:_$15_or_Less'):
    # listofFindCommands.append(dict_Average_Price_15_or_Less)

    ###########SHARED GENRES AND PUBLISHER CALLS TO DATABASE##################################
    if (filter == 'Average_Playtime:_30_minutes_or_Less'):
        listofFindCommands.append(dict_Average_Playtime_30_minutes_or_Less)
    if (filter == 'Average_Playtime:_1_Hour_or_Less'):
        listofFindCommands.append(dict_Average_Playtime_1_Hour_or_Less)
    if (filter == 'Average_Playtime:_1_Hour_or_More'):
        listofFindCommands.append(dict_Average_Playtime_1_Hour_or_More)
    if (filter == 'Average_Playtime:_30_Minutes_or_More'):
        listofFindCommands.append(dict_Average_Playtime_30_Minutes_or_More)

    ###########PUBLISHER CALLS TO DATABASE######################################
    if (filter == 'Average_Price:_$30_or_More_Double'):
        listofFindCommands.append(dict_Average_Price_30_or_More)
    if (filter == 'Average_Price:_$30_or_Less_Publisher'):
        listofFindCommands.append(dict_Average_Price_30_or_Less)
    if (filter == 'Average_Price:_$15_or_Less_Publisher'):
        listofFindCommands.append(dict_Average_Price_15_or_Less)

    basedictionary = {"$and": listofFindCommands}
    return ApplyFoundFilters(NonFilteredCollection,
                             basedictionary)  # This function returns filtered collection


def ApplyFoundFilters(NonFilteredCollection, basedictionary):
    # NonFilteredCollection is boardgame collections. This is used as a super collection.
    filteredCollection = db["FinalFiltered"]
    filteredCollection.drop()  # drop entire collection
    filteredCollection = db["FinalFiltered"]

    cur = NonFilteredCollection.find(basedictionary)
    for element in cur:
        # print(element)
        filteredCollection.insert_one(element)
    return filteredCollection  # This collection should be totally filtered


if __name__ == "__main__":
    app.run(debug=True)
