import mongoengine as me
from daos.daoLevels import Level

class LevelRating(me.EmbeddedDocument):
    idLevel = me.IntField(required=True)
    rating = me.FloatField(required=True)

class User(me.Document):
    username = me.StringField(primary_key=True)
    password = me.StringField(required=True)
    isAdmin = me.BooleanField(required=True, default=False)
    blocked = me.BooleanField(required=True, default=False)
    levelsCreated = me.ListField(me.ReferenceField(Level, reverse_delete_rule=me.PULL)) # me.ListField(me.IntField())
    levelsRating = me.ListField(me.EmbeddedDocumentField(LevelRating))
