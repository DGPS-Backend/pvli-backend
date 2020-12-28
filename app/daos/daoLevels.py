import mongoengine as me

class UserRating(me.EmbeddedDocument):
    username = me.IntField(required=True)
    rating = me.FloatField(required=True)

class LevelRating(me.EmbeddedDocument):
    avg = me.FloatField() 
    ratingByUser = me.ListField(me.EmbeddedDocumentField(UserRating))

class Comment(me.EmbeddedDocument):
    timeStamp = me.ComplexDateTimeField() 
    username = me.StringField() 
    comment = me.StringField()

class Level(me.Document):

    id = me.IntField(primary_key=True)

    name = me.StringField(required=True)

    image = me.StringField()
    
    username = me.StringField()
    
    # Indica si el nivel ha sido bloqueado.
    blocked = me.BooleanField(required=True, default=False)

    # Lista de comentarios de los usuarios en este nivel.
    comments = me.ListField(me.EmbeddedDocumentField(Comment))
    
    # Lista de criticas de los usuarios a este nivel.
    rating = me.EmbeddedDocumentField(LevelRating)

    phaserObject = me.StringField(required=True)


