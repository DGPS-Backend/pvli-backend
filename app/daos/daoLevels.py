import mongoengine as me

class Level(me.Document):
    id = me.StringField(primary_key=True)
    name = me.StringField(required=True)
    image = me.StringField(required=False)
    # Usuario que lo crea
    userName = me.StringField(required=False)
    # Comentarios de todos los usuarios
    comments = me.StringField(required=True)
    # Almacena si el nivel ha sido bloqueado
    blocked = me.StringField(required=True)
    # Media de las puntuaciones de todos los usuarios
    rating = me.StringField(required=True)
    # Número de usuarios que han puntuado el nivel (para actualizar el valor anterior)
    # rate_count = me.StringField(required=True)
    phaserObject = me.StringField(required=True)
