#If you're unsure what's happening here feel free to ask me (Sanne)
import requests
import xml.etree.ElementTree as ET
import main



def PublisherNames():
    #Function now returns tupple of list to so game and publisher are tied for publisher page elements.
    bgc = main.boardgameobjects.find()
    publishernames = []

    for game in bgc:
        if game['Publisher'] not in publishernames:
            publishernames.append(game['Publisher'])
    print (publishernames) #Debuggin
    return publishernames


ListofPublishers = PublisherNames() # Get all publishers we are using, this is from DB and filtered and built in main.oy



#Board Game Geek uses xml instead of json, so the interpreting of data is different
#This goes up pretty high, 810 at least
resp = requests.get("https://www.boardgamegeek.com/xmlapi/boardgamepublisher/3", stream=True)
response_as_string = resp.content
#print(response_as_string) #Print this line if you want to see how xml files look as strings
responseXml = ET.fromstring(response_as_string)
CompanyName = responseXml.find('company').find('name')
print(CompanyName.text)
CompanyDescription = responseXml.find('company').find('description')
print(CompanyDescription.text)


