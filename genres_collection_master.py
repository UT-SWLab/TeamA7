#This code updates all genres in the genres collection. If the collection is empty, it will populate it with our 72 genres. 
#If this code is run while the collection already has all of our genres in it, it will just update the genres, and shouldn't cause any duplicates.
#If you need to clear the entire collection, see the code at the very bottom of the file.
#Let me (Allegra) know if you have any questions before you try to run this.

import pymongo
from pymongo import MongoClient
from mongoengine import *
import requests

#connects to our MongoDB server running on MongoDB Atlas
client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
connect('BGDB', host='localhost', port=27017)

#designate 'db' as the name of our database to be used in this code, and 'boardgamecollection' as the name of the collection of board games to be used in this code
db = client["BGDB"]
boardgamecollection = db["boardgamecollection"]
genrecollection = db["genrecollection"]


###############################TO COLLECT ALL GAMES AND PUBLISHERS ASSOCIATED WITH EACH GENRE######################################

for game in boardgamecollection.find():
	for genre in game["genres"]:
		query = {"Name": genre}
		if genrecollection.find_one(query) != None:
			genretoupdate = genrecollection.find_one(query)
			print(genretoupdate["Name"])
			#to connect publishers to genres
			publisher = game['Publisher']
			genrecollection.update_one({'Name': genre}, { "$addToSet" : {"Publishers": publisher}})
			#to connect games to genres
			gamename = game['Name']
			genrecollection.update_one({'Name': genre}, { "$addToSet" : {"Games": gamename}})
		else:
			newgenre = {
				"Name": genre,
				"Games": [game['Name']],
				"Publishers": [game['Publisher']]
			}
			genrecollection.insert_one(newgenre)



#####################################TO FIND IMAGES TO USE ON THE GENRE INSTANCE PAGES############################################

#API request from Google Images
#uses API key generated on GCP to search custom search engine (also generated in GCP) that only searches Board Game Geek and Wikipedia
#safe search is on and results return exactly one image

for genre in genrecollection.find():
    name = genre["Name"]
    searchname = genre['Name'].replace(" ", "+") + "+board+games"
    requeststring = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCxFCh2XeiGTNT7kjDN2fhfB_J3W0ByabY&cx=4366fe0d278a82053&num=1&searchType=image&imgSize=large&q=" + searchname
    resp = requests.get(requeststring)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    else:
        results = resp.json()['items']
        formattedresults = results[0]
        image_url = formattedresults['link']
        genrecollection.update_one({'Name': name}, { "$set" : {"Image_URL": image_url}})



######################################################CLEAR COLLECTION#############################################################

#If for some reason you need to delete the collection entirely, comment out everything in this file besides the code below, then run.

#client = MongoClient("mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
#connect('BGDB', host='localhost', port=27017)

#db = client["BGDB"]
#genrecollection = db["genrecollection"]
# genrecollection.delete_many({ })