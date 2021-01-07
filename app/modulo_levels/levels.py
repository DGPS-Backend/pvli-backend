from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoUsers import User, LevelRating
from daos.daoLevels import Level, UserRating, Comment
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError
from random import randint

max_level_id = 999999999999

levels = Blueprint("levels", __name__)

# Loadlevels - Sensible a las mayus, ordenar x puntuaciones -M
# loadlevel - devolver nulo en el user si no hay creador de nivel -B OK
# storelevel - coleccion de contadores -B OK
# rate - if else para actualizar o insertar -M
# erase - comprobar si el nivel existe, cascade -a medias OK Manu maquinon

@levels.route('/loadLevels', methods=['POST'])
def loadLevels():

    # print("/loadLevels RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    try:

        if ("filter_text" in data):

            # Busca un nivel que contenga el texto que viene en el campo del filtro.
            levels = Level.objects(name__icontains=data["filter_text"]).order_by('-rating.avg')

            response = jsonify({"return_code": 200, "message": "OK", "games": levels.to_json()}), 200

        else:

            # Devolver los niveles del modo historia.
            levels = Level.objects()

            response = jsonify({"return_code": 200, "message": "OK", "games": levels.to_json()}), 200

    except ValidationError:
        response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
    except ServerSelectionTimeoutError:
        response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response

@levels.route('/loadLevel', methods=['POST'])
def loadLevel():

    '''
    Devolver nulo si es necesario. READY 4 BASILIO
    '''

    print("/loadLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    if ("id_level" in data):

        try:

            level = Level.objects(id=data["id_level"]).get()

            name = level.name
            image = level.image
            blocked = level.blocked
            json = level.phaserObject
            userName = level.username
            comments = level.comments

            avg = level.rating.avg
            if avg == -1 :
                avg = None

            response = jsonify({"return_code": 200,
                                "message": "OK",
                                "json": json,
                                "name_level": name,
                                "img": image,
                                "id_user": userName,
                                "comments": comments,
                                "blocked": blocked,
                                "rate": avg,
                                }), 200

        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response

@levels.route('/storeLevel', methods=['POST'])
def storeLevel():

    '''
    Crear una coleccion de contadores. OK LISTO EVARISTO
    '''

    print("/storeLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    if ("name_level" in data) and ("username" in data) and ("json" in data) :

        try:

            # Crea un objeto de tipo nivel.
            level = Level(name=data["name_level"],
                          username=data["username"],
                          phaserObject=data["json"])

            # Obtener id autoincremental
            id = level.id

            # Guardamos el nivel en la base de datos.
            level.save(force_insert=True)

            # Guarda en el array de niveles del usuario la referencia al nivel.
            User.objects(username=data["username"]).update_one(push__levelsCreated=level)

            response = jsonify({"return_code": 200, "message": "OK", "id": id, "json": data["json"]}), 200

        except NotUniqueError:
            response = jsonify({"return_code": 601, "message": "User exists"}), 601
        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response

@levels.route('/commentLevel', methods=['PUT'])
def commentLevel():

    # print("/commentLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    if ("id_level" in data) and ("id_user" in data) and ("comment" in data):

        try:

            Level.objects(id=data["id_level"]).update_one(push__comments=Comment(username=data["id_user"], comment=data["comment"]))

            response = jsonify({"return_code": 200, "message": "OK"}), 200

        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response

@levels.route('/rateLevel', methods=['PUT'])
def rateLevel():

    print("/rateLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data) and ("id_user" in data) and ("rate" in data):

        try:

            # Comprobamos si el usuario ya valoró el nivel.
            user = User.objects(username=data["id_user"], levelsRating__idLevel=data["id_level"])

            # Si el usuario no había valorado el nivel.
            if len(user) == 0:

                # Insertamos por vez primera la crítica en la lista de críticas del usuario.
                User.objects(username=data["id_user"]).update_one(push__levelsRating=LevelRating(idLevel=data["id_level"], rating=data["rate"]))

                # Insertamos por vez primera la crítica en la lista de críticas del nivel.
                Level.objects(id=data["id_level"]).update_one(push__rating__ratingByUser=UserRating(username=data["id_user"], rating=data["rate"]))

            else:

                # Actualiza la crítica en la lista del usuario.
                user.update_one(set__levelsRating__S__rating=data["rate"])

                # Actualiza la crítica en la lista del nivel.
                Level.objects(id=data["id_level"], rating__ratingByUser__username=data["id_user"]).update_one(set__rating__ratingByUser__S__rating=data["rate"])

            # Calcula la media del nivel.
            info = Level.objects(id=data["id_level"]).aggregate({"$project": { "average": { "$avg": "$rating.ratingByUser.rating" } } })

            # Obtengo un diccionario con el id del nivel y la media de sus puntuaciones.
            info = dict(list(info)[0])

            # Establezco la media del nivel una vez recalculada.
            Level.objects(id=data["id_level"]).update_one(set__rating__avg=info["average"])

            response = jsonify({"return_code": 200, "message": "OK"}), 200

        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response

@levels.route('/eraseLevel', methods=['POST'])
def eraseLevel():

    # print("/eraseLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    if ("id_level" in data):

        try:

            level = Level.objects(id=data["id_level"])

            # Si no se encontró el nivel, devolvemos fallo, en caso contrario borramos y avisamos de ello.
            if len(level) == 0:
                response = jsonify({"return_code": 602, "message": "Level doesn't exits"}), 602
            else:
                level.delete() # Borra el objeto y la referencia en el array del usuario.
                response = jsonify({"return_code": 200, "message": "OK"}), 200

        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response
