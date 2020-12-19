import mongoengine as me

class Usuarios(me.Document):
    username = me.StringField(primary_key=True)
    password = me.StringField(required=True)
