import mongoengine as me

class Level(me.Document):
    id_level = me.StringField(primary_key=True)
    json_phaser = me.StringField(required=True)
