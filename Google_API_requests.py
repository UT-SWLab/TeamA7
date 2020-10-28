#you may need to download some of these things to get this code (or similar code) to work
#let me (Allegra) know if you have any questions
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

#API request from Google Images
#uses API key generated on GCP to search custom search engine (also generated in GCP) that only searches Google Images
#safe search is on and results return exactly one image of large size


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