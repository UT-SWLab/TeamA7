#This code updates all games in the games collection. If the collection is empty, it will populate it with our 123 games. 
#If this code is run while the collection already has all of our games in it, it will just update the games, and shouldn't cause any duplicates.
#If you need to clear the entire collection, see the code at the very bottom of the file.
#Let me (Allegra) know if you have any questions before you try to run this.

import pymongo
from pymongo import MongoClient
from mongoengine import *
import requests
import time
import re

#connects to our MongoDB server running on MongoDB Atlas
#commented out for safety to prevent people who don't know how it works from running it, uncomment to actually run
#client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
#connect('BGDB', host='localhost', port=27017)

#designate 'db' as the name of our database to be used in this code, and 'boardgamecollection' as the name of the collection of board games to be used in this code
db = client["BGDB"]
boardgamecollection = db["boardgamecollection"]

############################################TO PUT FIRST 100 GAMES IN COLLECTION####################################################

# API request from Board Game Atlas
resp = requests.get('https://api.boardgameatlas.com/api/search?list_id=L6t9vL6DnV&client_id=zJUSH9XolY')

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for game in resp.json()['games']:

    # you have to make a dictionary object with the info and then insert that into the collection
    newboardgame = {
        "Name": game['name'],
        "Game_ID": game['id'],
        "Category": [game['categories']],
        "Publisher": game['publishers'][0],
        "Description": game['description'],
        "Min_Players": game['min_players'],
        "Max_Players": game['max_players'],
        "Min_Playtime": game['min_playtime'],
        "Max_Playtime": game['max_playtime'],
        "Year_Published": game['year_published'],
        "Min_Age": game['min_age'],
        "Image_URL": game['image_url'],
        "BGA_Link": game['url'],
        "Current_Price": game['price'],
        "Suggested_Retail_Price": game['msrp'],
        "Discount": game['discount'],
        "Designers": game['designers'],
        "Developers": game['developers'],
        "Artists": game['artists'],
        "BGA_Num_User_Ratings": game['num_user_ratings'],
        "BGA_Average_User_Rating": game['average_user_rating'],
        "Rules_URL": game['rules_url']
    }

    # insert the new board game into the board game collection or update the existing board game by replacing the information
    boardgamecollection.replace_one({'Name': newboardgame['Name']}, newboardgame, upsert=True)

############################################TO PUT GAMES 101-123 IN COLLECTION######################################################

#API request from Board Game Atlas
resp = requests.get('https://api.boardgameatlas.com/api/search?skip=100&list_id=L6t9vL6DnV&client_id=zJUSH9XolY')

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for game in resp.json()['games']:

    # you have to make a dictionary object with the info and then insert that into the collection
    newboardgame = {
        "Name": game['name'],
        "Game_ID": game['id'],
        "Category": [game['categories']],
        "Publisher": game['publishers'][0],
        "Description": game['description'],
        "Min_Players": game['min_players'],
        "Max_Players": game['max_players'],
        "Min_Playtime": game['min_playtime'],
        "Max_Playtime": game['max_playtime'],
        "Year_Published": game['year_published'],
        "Min_Age": game['min_age'],
        "Image_URL": game['image_url'],
        "BGA_Link": game['url'],
        "Current_Price": game['price'],
        "Suggested_Retail_Price": game['msrp'],
        "Discount": game['discount'],
        "Designers": game['designers'],
        "Developers": game['developers'],
        "Artists": game['artists'],
        "BGA_Num_User_Ratings": game['num_user_ratings'],
        "BGA_Average_User_Rating": game['average_user_rating'],
        "Rules_URL": game['rules_url']
    }

    # insert the new board game into the board game collection or update the existing board game by replacing the information
    boardgamecollection.replace_one({'Name': newboardgame['Name']}, newboardgame, upsert=True)


###########################################TO POPULATE INFORMATION FOR ALL GAMES IN COLLECTION#############################################

# when we reach 60 requests, we need to sleep for one minute in order to avoid exceeding our request limit of 60 per minute
# to allow for wiggle room, this code sleeps for 62 seconds when we reach 55 requests
count = 0

def updatecount():
    global count
    count += 1
    if count >=55:
        count = 0
        time.sleep(62)

#API request from Board Game Atlas, to get category names
categoriesresp = requests.get('https://api.boardgameatlas.com/api/game/categories?name=Aliens&client_id=zJUSH9XolY')
categoriesfromBGA = categoriesresp.json()["categories"]
genres = {}
for cat in categoriesfromBGA:
    g = {cat['id']: cat['name']}
    genres.update(g)

#HTML tags to parse out from game descriptions (not all tags need to be parsed because MongoDB is weird)
tagstodelete = {"<b>", "</b>", "<i>", "</i>", "<strong>", "</strong>", "<div>", "</div>", "<p>", "<em>", "</em>", "<ul>", "</ul>", "<li>", "&quot;", "<h4>"}
tagstoreplacewithspace = {"</p>", "</li>", "</h4>"}

#need batch size so that cursor doesn't time out
for game in boardgamecollection.find().batch_size(50):

    game_id = game['Game_ID']


    ###########################TO UPDATE THE CATEGORIES TO ACTUAL NAMES INSTEAD OF CATEGORY IDS##########################

    c = game['Category']
    genresforgame = []
    for i in c:
        for o in i:
            if o['id'] in genres:
                genresforgame.append(genres[o['id']])
    boardgamecollection.update_one({'Name': game['Name']}, {"$set" : {"genres": genresforgame}})
    #delete old Category array
    boardgamecollection.update_one({'Name': game['Name']}, {"$unset" : {"Category": ""}})


    ###################################TO PARSE OUT THE HTML TAGS FROM DESCRIPTIONS######################################

    description = game["Description"]

    for tag in tagstodelete:
        description = description.replace(tag, "")

    for tag in tagstoreplacewithspace:
        description = description.replace(tag, " ")

    boardgamecollection.update_one({'Name': game['Name']}, {"$set" : {"Description": description}})


    ############################################TO GET EXTRA GAME IMAGES################################################

    updatecount()
    #API request from Board Game Atlas
    request = "https://api.boardgameatlas.com/api/game/images?limit=10&client_id=zJUSH9XolY&game_id=" + game_id
    resp = requests.get(request)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for image in resp.json()['images']:
        boardgamecollection.update_one({'Name': game['Name']}, {"$addToSet" : {"Images": image['url']}})


    ############################################TO GET GAME VIDEOS######################################################

    updatecount()
    #API request from Board Game Atlas
    request = "https://api.boardgameatlas.com/api/game/videos?limit=10&client_id=zJUSH9XolY&game_id=" + game_id
    resp = requests.get(request)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for video in resp.json()['videos']:
        newvideo = {'Title': video['title'], 'URL': video['url']} 
        boardgamecollection.update_one({'Name': game['Name']}, {"$addToSet" : {"Videos": newvideo}})


    #######################################TO GET GAME REDDIT COMMENTS##################################################

    updatecount()
    #API request from Board Game Atlas
    request = "https://api.boardgameatlas.com/api/game/reddit?limit=10&client_id=zJUSH9XolY&game_id=" + game_id
    resp = requests.get(request)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for comment in resp.json()['reddit_comments']:
        body = comment['body']
        #parse out HTML tags
        parsetags = re.compile('<.*?>')
        cleanbody = re.sub(parsetags, '', body)
        newcomment = {'Title': comment['title'], 'URL': comment['link_url'], 'Body': cleanbody} 
        boardgamecollection.update_one({'Name': game['Name']}, {"$addToSet" : {"Reddit_Comments": newcomment}})


##############################################CLEAR COLLECTION###########################################################

#If for some reason you need to delete the collection entirely, comment out everything in this file besides the code below, then run.

#client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
#connect('BGDB', host='localhost', port=27017)

#db = client["BGDB"]
#boardgamecollection = db["boardgamecollection"]
#boardgamecollection.delete_many({ })