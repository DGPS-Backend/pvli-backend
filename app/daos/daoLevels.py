import mongoengine as me

class Level(me.Document):
    id_level = me.StringField(primary_key=True)
    name_level = me.StringField(required=True)
    json_phaser = me.StringField(required=True)
    # Media de las puntuaciones de todos los usuarios
    rate = me.StringField(required=True)
    # Número de usuarios que han puntuado el nivel (para actualizar el valor anterior)
    rate_count = me.StringField(required=True)
    # Comentarios de todos los usuarios
    comments = me.StringField(required=True)
    # Almacena si el nivel ha sido bloqueado
    blocked = me.StringField(required=True)
