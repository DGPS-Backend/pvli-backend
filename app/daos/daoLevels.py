import mongoengine as me

class Level(me.Document):
    id = me.IntField(primary_key=True)

    name = me.StringField(required=True)

    image = me.StringField()
    # Usuario que lo crea, no es obligatorio porque puede estar hecho de antes
    userName = me.StringField() # REVISAR MODELO DEL DOMINIO
    # Comentarios de todos los usuarios
    comments = me.ListField(me.StringField(), required=True) # COMO SE HACE ESTA MIERDA TODOTDO
    # # Almacena si el nivel ha sido bloqueado
    blocked = me.BooleanField(required=True)
    # # Media de las puntuaciones de todos los usuarios
    # rating = me.ListField(me.IntField(), required=True)

    phaserObject = me.StringField(required=True)

class LevelRating(me.Document):
    # ID del nivel
    id = me.IntField(primary_key=True)
    avg = me.FloatField(required=True)
    ratingByUser = me.ListField(me.IntField(), required=True) # MECAGUEN COMO SE METE EL USUARIO AQUI
