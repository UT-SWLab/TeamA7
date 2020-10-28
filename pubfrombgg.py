# If you're unsure what's happening here feel free to ask me (Sanne)
import requests
import xml.etree.ElementTree as ET
import main

DictNameToPublisherID = {"Stronghold Games": "11652",
                         "CMON": "21608        ",
                         "Hasbro": "   51        ",
                         "None": "   None        ",
                         " Matagot": "   5400        ",
                         "Rio Grande Games": "    3        ",
                         "Gozer Games LLC": "   25842        ",
                         "Space Cowboys": "  25842        ",
                         "Jolly Roger Games": "   206        ",
                         "Playroom Entertainment": "    244        ",
                         "Gamewright": "   108        ",
                         "PD-Verlag": "   8401        ",
                         "Secret Hitler": "     None        ",
                         "IELLO": "     8923        ",
                         "Fantasy Flight Games": "      17        ",
                         "Brain Games": "     7162        ",
                         "Die-Hard Games LLC": "   28148        ",
                         "Grail Games": "   27311        ",
                         "Wizards of the Coast": "   13        ",
                         "Avalon Hill Games, Inc. ": "       4871        ",
                         "R&D Games": "   83        ",
                         "Game Salute": "    22701        ",
                         "KOSMOS": "     37        ",
                         "NSKN Games": "    18529        ",
                         "Bezier Games": "    5774        ",
                         "Splotter Spellen": "    140        ",
                         "Czech Games Edition": "       7345        ",
                         "Gen Four Two Games": "      None        ",
                         "Indie Boards and Cards": "     10290        ",
                         "Renegade Game Studios": "     28072        ",
                         "Arcane Wonders": "   17812        ",
                         "Plan B Games": "    34188        ",
                         "Asmodee Editions": "    None        ",
                         "Lookout Games": "     234        ",
                         "Grey Fox Games": "   place        ",
                         "Alderac Entertainment Group": "     place        ",
                         "Pandasaurus Games": "     place        ",
                         "WizKids": "   place        ",
                         "Ceaco": "  place        ",
                         "Flat River Group": "  place        ",
                         "Z-Man Games": "       place        ",
                         "Libellud": "       place        ",
                         "Indie Boards & Cards": "       place        ",
                         "ABACUSSPIELE": "       place        ",
                         "PSIQ7": " place        ",
                         "Thames & Kosmos": "       place        ",
                         "Fantasy Flight Publishing": "       place        ",
                         "Days of Wonder": "      place        ",
                         "Garphill Games": "      place        ",
                         "Publisher Services Inc (PSI)": "       place        ",
                         "Floodgate Games": "       place        ",
                         "Plaid Hat Games": "      place        ",
                         "North Star Games": "      place        ",
                         "Blue Cocker": "      place        ",
                         "Karma Games": "     place        ",
                         "White Wizard Games": "       place        ",
                         "Blue Orange Games": "      place        ",
                         "Eggertspiele": "      place        ",
                         "Spin Master": "      place        ",
                         "Roxley": "     place        ",
                         "Ravensburger": "      place        ",
                         "Hans im Glück": "      place        ",
                         "Repos Production": "      place        ",
                         "Z-Man Games, Inc": "      place        ",
                         "Greater Than Games": "       place        ",
                         "Next Move Games": "       place        ",
                         "Stonemaier Games": "      place        ",
                         "Leder Games": "       place        ",
                         "Cephalofair Games": "      place        ", }


def PublisherNames():
    # Function now returns tupple of list to so game and publisher are tied for publisher page elements.
    bgc = main.boardgameobjects.find()
    publishernames = []

    for game in bgc:
        if game['Publisher'] not in publishernames:
            publishernames.append(game['Publisher'])
    print(publishernames)  # Debuggin
    return publishernames


ListofPublishers = PublisherNames()  # Get all publishers we are using, this is from DB and filtered and built in main.oy

# Board Game Geek uses xml instead of json, so the interpreting of data is different
# This goes up pretty high, 810 at least
resp = requests.get("https://www.boardgamegeek.com/xmlapi/boardgamepublisher/83", stream=True)
response_as_string = resp.content
# print(response_as_string) #Print this line if you want to see how xml files look as strings
responseXml = ET.fromstring(response_as_string)
CompanyName = responseXml.find('company').find('name')
print(CompanyName.text)
CompanyDescription = responseXml.find('company').find('description')
print(CompanyDescription.text)
