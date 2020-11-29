from pymongo import MongoClient
import pymongo
from mongoengine import *
# Source for Factory Method Implementation with Python:
# https://www.geeksforgeeks.org/factory-method-python-design-patterns/
client = MongoClient(
    "mongodb+srv://teama7:ee461lteama7@mongodbcluster.bs58o.gcp.mongodb.net/BGDB?retryWrites=true&w=majority")
db = client["BGDB"]
connect('BGDB', host='localhost', port=27017)
board_game_objects = db.boardgamecollection
genre_objects = db.genrecollection
publisher_objects = db.publishercollection

# input = string searched by user
# models = list of string terms for each model type
# fields = list of strings for each field to search
def searchdb(input, models, fields):
    exactmatches = {}  # not case sensitive, array of all exact matches
    partialmatches = {}  # not case sensitive, dict of all partial matches with key the word they're matched to
    words_in_input = list(input.split())
    searchers = searchFactory(models, fields)
    for s in searchers:
        exactmatches.update(s.search_for_string(input))
    if len(words_in_input) > 1:
        for w in words_in_input:
            results_for_word = {}
            for s in searchers:
                results_for_word.update(s.search_for_string_with_exclusion(w, input))
            partialmatches.update({w: results_for_word})
    return exactmatches, partialmatches


class SearchBoardGames:
    def __init__(self, fields):
        if fields == ['all']:
            self.fields = ["Name", "Description", "Publisher", "genres"]
            return
        board_game_fields = ["Name", "Description", "Publisher", "genres"]
        for f in board_game_fields:
            if f in fields:
                self.fields.append(f)

    def search_for_string(self, input):
        return {'boardgames': list(board_game_objects.find(search_dictionary(self.fields, input)))}

    def search_for_string_with_exclusion(self, word, input):
        return {'boardgames': list(board_game_objects.find(search_dict_with_exclusions(self.fields, word, input)))}


class SearchGenres:
    def __init__(self, fields):
        if fields[0] == 'all':
            self.fields = ["Name", "Description", "Publishers", "Games"]
            return
        genre_fields = ["Name", "Description", "Publishers", "Games"]
        for f in genre_fields:
            if f in fields:
                self.fields.append(f)

    def search_for_string(self, input):
        return {'genres': list(genre_objects.find(search_dictionary(self.fields, input)))}

    def search_for_string_with_exclusion(self, word, input):
        return {'genres': list(genre_objects.find(search_dict_with_exclusions(self.fields, word, input)))}


class SearchPublishers:
    def __init__(self, fields):
        if fields[0] == 'all':
            self.fields = ["Name", "Description", "Genres", "Games"]
            return
        publisher_fields = ["Name", "Description", "Genres", "Games"]
        for f in publisher_fields:
            if f in fields:
                self.fields.append(f)

    def search_for_string(self, input):
        return {'publishers': list(publisher_objects.find(search_dictionary(self.fields, input)))}

    def search_for_string_with_exclusion(self, word, input):
        return {'publishers': list(publisher_objects.find(search_dict_with_exclusions(self.fields, word, input)))}


def search_dictionary(fields, input):
    search_dictionary = {"$or": []}
    for f in fields:
        search_dictionary["$or"].append({f: {"$regex": ".*" + input + ".*", '$options': 'i'}})
    return search_dictionary


def search_dict_with_exclusions(fields, word, input):
    search_dictionary = {"$or": []}
    for f in fields:
        search_dictionary["$or"].append({"$and": [{f: {"$regex": ".*" + word + ".*", '$options': 'i'}},
                                                  {f: {"$not": {"$regex": ".*" + input + ".*", '$options': 'i'}}}]})
    return search_dictionary


def searchFactory(models, fields):
    possible_searchers = {'boardgames': SearchBoardGames, 'genres': SearchGenres, 'publishers': SearchPublishers}
    searchers = []
    for m in models:
        searchers.append(possible_searchers[m](fields))
    return searchers