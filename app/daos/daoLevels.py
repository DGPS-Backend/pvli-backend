import mongoengine as me
from datetime import datetime as dt

class UserRating(me.EmbeddedDocument):
    username = me.StringField(required=True)
    rating = me.FloatField(required=True)

class LevelRating(me.EmbeddedDocument):
    avg = me.FloatField(required=True)
    ratingByUser = me.ListField(me.EmbeddedDocumentField(UserRating))

class Comment(me.EmbeddedDocument):
    timestamp = me.DateTimeField(required=True, default=dt.utcnow)
    username = me.StringField(required=True)
    comment = me.StringField(required=True)

# class AutoIncId(me.EmbeddedDocument):
#     cont = me.SequenceField(required=True)

class Level(me.Document):

    id = me.SequenceField(primary_key=True)

    name = me.StringField(required=True)

    image = me.StringField()

    username = me.StringField()

    # Indica si el nivel ha sido bloqueado.
    blocked = me.BooleanField(required=True, default=False)

    # Lista de comentarios de los usuarios en este nivel.
    comments = me.ListField(me.EmbeddedDocumentField(Comment))

    # Lista de criticas de los usuarios a este nivel.
    rating = me.EmbeddedDocumentField(LevelRating, required=True, default=LevelRating(avg=-1))

    phaserObject = me.StringField(required=True)
