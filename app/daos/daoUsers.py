import mongoengine as me

class LevelRating(me.EmbeddedDocument):
    idLevel = me.IntField(required=True)
    rating = me.FloatField(required=True)

class User(me.Document):
    username = me.StringField(primary_key=True)
    password = me.StringField(required=True)
    isAdmin = me.BooleanField(required=True, default=False)
    blocked = me.BooleanField(required=True, default=False)
    levelsCreated = me.ListField(me.IntField())
    levelsRating = me.ListField(me.EmbeddedDocumentField(LevelRating))
