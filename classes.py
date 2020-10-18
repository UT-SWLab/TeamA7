import pymongo
from mongoengine import *

class BoardGame(Document):
    name = StringField(required=True)
    categories = ListField(StringField())
    publisher = StringField()
    description = StringField()
    min_players = IntField()
    max_players = IntField()
    min_playtime = IntField()
    max_playtime = IntField()
    year_published = IntField()
    min_age = IntField()
    image_url = StringField()
    website = StringField()

class Category(Document):
	name = StringField(required=True)
	description = StringField()

class Publisher(Document):
	name = StringField(required=True)
	description = StringField()