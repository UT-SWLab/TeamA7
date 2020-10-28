# If you're unsure what's happening here feel free to ask me (Cedrik)
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
publishercollection = db["publishercollection"]


#We loop it into super dict and then just push super DICT to DB
publisherSuperDict = DictNameToPublisherID = {
"Stronghold Games": "Founded in late 2009, the focus of Stronghold Games has been to provide maximum customer value by delivering high-quality products, and maximum customer satisfaction with Best of Breed games, i.e. games that are the finest in mechanic, theme, and/or other attributes valued by gamers."
,}

publishercollection.insert_one(publisherSuperDict)

#to clear the collection
#boardgamecollection.delete_many({ })







'''
DictNameToPublisherID = {"Stronghold Games": "11652",
                         "CMON": "21608",
                         "Hasbro": "51",
                         "None": "None",
                         "Matagot": "5400",
                         "Rio Grande Games": "3",
                         "Gozer Games, LLC": "25842",
                         "Space Cowboys": "  25842",
                         "Jolly Roger Games": "206",
                         "Playroom Entertainment": "244",
                         "Gamewright": "108",
                         "PD-Verlag": "8401",
                         "Secret Hitler": "None",
                         "IELLO": "8923",
                         "Fantasy Flight Games": "7",
                         "Brain Games": "7162",
                         "Die-Hard Games LLC": "28148",
                         "Grail Games": "27311",
                         "Wizards of the Coast": "13",
                         "Avalon Hill Games, Inc. ": "4871",
                         "R&D Games": "83",
                         "Game Salute": "22701",
                         "KOSMOS": "37",
                         "NSKN Games": "18529",
                         "Bezier Games": "5774",
                         "Splotter Spellen": "140",
                         "Czech Games Edition": "7345",
                         "Gen Four Two Games": "None",
                         "Indie Boards and Cards": "10290",
                         "Renegade Game Studios": "28072",
                         "Arcane Wonders": "17812",
                         "Plan B Games": "34188",
                         "Asmodee Editions": "None",
                         "Lookout Games": "234",
                         "Grey Fox Games": " place",
                         "Alderac Entertainment Group": "place",
                         "Pandasaurus Games": "place",
                         "WizKids": "place",
                         "Ceaco": "place",
                         "Flat River Group": "place",
                         "Z-Man Games": "place",
                         "Libellud": "place ",
                         "Indie Boards & Cards": "place",
                         "ABACUSSPIELE": "place",
                         "PSIQ7": "place",
                         "Thames & Kosmos": "place",
                         "Fantasy Flight Publishing": "place",
                         "Days of Wonder": "place",
                         "Garphill Games": "place",
                         "Publisher Services Inc (PSI)": "place",
                         "Floodgate Games": "place",
                         "Plaid Hat Games": "place",
                         "North Star Games": "place",
                         "Blue Cocker": "place",
                         "Karma Games": "place",
                         "White Wizard Games": "place",
                         "Blue Orange Games": "place",
                         "Eggertspiele": "place",
                         "Spin Master": "place",
                         "Roxley": "place",
                         "Ravensburger": "place",
                         "Hans im Glück": "place ",
                         "Repos Production": "place",
                         "Z-Man Games, Inc": "place",
                         "Greater Than Games": "place",
                         "Next Move Games": "place",
                         "Stonemaier Games": "place ",
                         "Leder Games": "place",
                         "Cephalofair Games": "place", }


def PublisherNames():
    # Function now returns tupple of list to so game and publisher are tied for publisher page elements.
    bgc = main.boardgameobjects.find()
    publishernames = []

    for game in bgc:
        if game['Publisher'] not in publishernames:
            publishernames.append(game['Publisher'])
    print(publishernames)  # Debuggin
    return publishernames


def removeNone(ListofPublishers):
    for i in ListofPublishers:
        if i == " None": ListofPublishers.remove(i)
    return ListofPublishers


ListofPublishers = PublisherNames()  # Get all publishers we are using, this is from DB and filtered and built in main.oy
ListofPublishers = removeNone(ListofPublishers)

print(ListofPublishers)

DictLocalCpName_CpDescription = {}

for i in ListofPublishers:
    print(i)
    if i == "None":
        continue
    publisherID = DictNameToPublisherID.get(i)
    print(publisherID)
    # Board Game Geek uses xml instead of json, so the interpreting of data is different
    # This goes up pretty high, 810 at least
    if publisherID == "None" or publisherID == "place":
        continue
    time.sleep(5)

    resp = requests.get("https://www.boardgamegeek.com/xmlapi/boardgamepublisher/" + str(publisherID), stream=True)
    response_as_string = resp.content
    print(response_as_string)  # Print this line if you want to see how xml files look as strings
    responseXml = ET.fromstring(response_as_string)
    CompanyName = responseXml.find('company').find('name')
    CompanyName = CompanyName.text
    CompanyDescription = responseXml.find('company').find('description')
    CompanyDescription = CompanyDescription.text
    DictLocalCpName_CpDescription.update({CompanyName: CompanyDescription})

print(DictLocalCpName_CpDescription)

'''