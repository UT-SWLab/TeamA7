from flask import Flask, render_template, url_for, request, redirect, session
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import *
import requests
import re
from search import searchdb

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

boardgame_filters = [
    "1_Hour_or_More",
    "1_Hour_or_Less",
    "30_Minutes_or_Less",
    "Players:_2",
    "Players:_3",
    "Players:_4",
    "Players:_5"
]

publisher_filters = [
    "Average_Price:_$30_or_More",
    "Average_Price:_$30_or_Less",
    "Average_Price:_$15_or_Less",
    "Average_Playtime:_30_Minutes_or_Less",
    "Average_Playtime:_30_Minutes_or_More"
]

genre_filters = [
    "Average_Price:_$30_or_More",
    "Average_Price:_$30_or_Less",
    "Average_Price:_$15_or_Less",
    "Average_Playtime:_30_Minutes_or_Less",
    "Average_Playtime:_30_Minutes_or_More"
]


def GameLinkify(name):
    linkformat = re.compile('[^a-zA-Z0-9]')
    linkname = linkformat.sub('', name)
    return linkname



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
    global boardgameobject
    filteredCollection = SelectFilter(filters, boardgameobjects)
    # Apply ordering to filtered collection.
    if sort_type == "alphabetical":
        gameobjects = filteredCollection.sort("Name")

    elif sort_type == "inverse":
        gameobjects = filteredCollection.sort("Name", -1)

    elif sort_type == "min-playtime":
        gameobjects = filteredCollection.sort("Min_Playtime")

    elif sort_type == "min-players":
        gameobjects = filteredCollection.sort("Min_Players")

    else:
        # Case where no sorting is done, Give Cursor to list_Base Page
        gameobjects = filteredCollection
    empty = filteredCollection.count() == 0
    max_pages = ((gameobjects.count() - 1) // 12) + 1
    return render_template('Board_Games_List.html', gameobjects=gameobjects, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgames', filters=filters, empty=empty,
                            filters_list=boardgame_filters, filter_title="Filters For Games")


@app.route('/boardgamegenres/<string:sort_type>/<int:page>/<string:filters>')
def genres(page, sort_type, filters):
    global genre_objects

    filteredCollection = SelectFilter(filters, genre_objects)

    if sort_type == "alphabetical":
        genre_obj = filteredCollection.sort("Name")
    elif sort_type == "inverse":
        genre_obj = filteredCollection.sort("Name", -1)

    elif sort_type == "min-playtime":
        genre_obj = filteredCollection.sort("Average_Min_Playtime")

    elif sort_type == "min-players":
        genre_obj = filteredCollection.sort("Average_Min_Players")
    else:
        genre_obj = filteredCollection
    empty = filteredCollection.count() == 0
    max_pages = ((genre_obj.count() - 1) // 12) + 1
    return render_template('Genres_List.html', genres=genre_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamegenres', filters=filters, empty=empty,
                            filters_list=genre_filters, filter_title="Filters For Genres")


@app.route('/boardgamepublishers/<string:sort_type>/<int:page>/<string:filters>')
def publishers(page, sort_type, filters):
    global publish_objects

    filteredCollection = SelectFilter(filters, publish_objects)
    if sort_type == "alphabetical":
        publish_obj = filteredCollection.sort("Name")
    elif sort_type == "inverse":
        publish_obj = filteredCollection.sort("Name", -1)

    elif sort_type == "min-playtime":
        publish_obj = filteredCollection.sort("Average_Min_Playtime")

    elif sort_type == "min-players":
        publish_obj = filteredCollection.sort("Average_Min_Players")

    else:
        publish_obj = filteredCollection

    empty = filteredCollection.count() == 0
    max_pages = ((publish_obj.count() - 1) // 12) + 1
    return render_template('Publishers_List.html', publishers=publish_obj, page=page, max_pages=max_pages,
                           sort_type=sort_type, page_route='boardgamepublishers', filters=filters,
                           empty=empty, filters_list=publisher_filters, filter_title="Filters For Publishers")


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
    return render_template("Genre_Template.html", genre=genre, boardgames=boardgameobjects, model=genre)


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
    return render_template("Publisher_Template.html", publisher=publisher, boardgames=boardgameobjects, model=publisher)


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
    models = []
    fields = ['all']
    if request.form["modeltype"] == 'all':
        models = ['boardgames', 'genres', 'publishers']
    else:
        models = [request.form["modeltype"]]
    if "fields" in request.form:
        fromform = request.form["fields"]
        if fromform != "all":
            fields = fromform.split(',')
    exactmatches, partialmatches = searchdb(input=input_string, models=models, fields=fields)

    return render_template("searchresults.html", input_string=input_string, exactmatches=exactmatches,
                           partialmatches=partialmatches, modeltype=type)


def noFilter(cur, filteredCollection):
    for match in cur.find():
        filteredCollection.insert_one(match)
    return filteredCollection



def SelectFilter(filter, NonFilteredCollection):
    if filter == "nofilters":
        return NonFilteredCollection.find()
    if (filter.split('_')[1]) == 'Hour':
        Minutes = int(filter.split('_')[0]) * 60
        if (filter.split('_')[3]) == 'More':
            return ApplyFoundFilters(NonFilteredCollection, {"Max_Playtime": {"$gte": Minutes}})
        else:
            return ApplyFoundFilters(NonFilteredCollection, {"Max_Playtime": {"$lte": Minutes}})

    if (filter.split('_')[1]) == 'Minutes':
        return ApplyFoundFilters(NonFilteredCollection, {"Max_Playtime": {"$lte": int(filter.split('_')[0])}})

    if (filter.split('_')[0]) == 'Players:':
        numberOfPlayers = int((filter.split('_')[1]).strip('+'))  # Necessary for 5 + case
        return ApplyFoundFilters(NonFilteredCollection, {"Min_Players": {"$lte": numberOfPlayers}, "Max_Players": {"$gte": numberOfPlayers}})

    if (filter.split('_')[1]) == 'Price:':
        Price = int(filter.split('_')[2].strip('$'))
        if (filter.split('_')[4]) == 'More':
            return ApplyFoundFilters(NonFilteredCollection, {"Average_Price_Float": {"$gte": Price}})
        if (filter.split('_')[4]) == 'Less':
            return ApplyFoundFilters(NonFilteredCollection, {"Average_Price_Float": {"$lte": Price}})

    if filter.split('_')[1] == 'Playtime:':
        if (filter.split('_')[3]) == 'Hour':
            Minutes = int(filter.split('_')[2]) * 60
            if (filter.split('_')[5]) == 'More':
                return ApplyFoundFilters(NonFilteredCollection, {"Average_Playtime": {"$gte": Minutes}})
            else:
                return ApplyFoundFilters(NonFilteredCollection, {"Average_Playtime": {"$lte": Minutes}})

        if (filter.split('_')[3]) == 'Minutes':
            if (filter.split('_')[5]) == 'More':
                return ApplyFoundFilters(NonFilteredCollection, {"Average_Playtime": {"$gte": int(filter.split('_')[2])}})
            else:
                return ApplyFoundFilters(NonFilteredCollection, {"Average_Playtime": {"$lte": int(filter.split('_')[2])}})
    return ApplyFoundFilters(NonFilteredCollection, null)  # This function returns filtered collection


def ApplyFoundFilters(NonFilteredCollection, basedictionary):
    return NonFilteredCollection.find(basedictionary) # This collection should be totally filtered


if __name__ == "__main__":
    app.run(debug=True)
