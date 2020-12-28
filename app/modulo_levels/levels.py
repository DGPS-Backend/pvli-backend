from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoLevels import Level, UserRating, Comment
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError
from random import randint

max_level_id = 999999999999

levels = Blueprint("levels", __name__)


@levels.route('/loadLevels', methods=['POST'])
def loadLevels():

    print("/loadLevels RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("filter_text" in data):
        try:
            # COMO NO ME DIGAS QUE OSTIAS VA EN EL FILTRO POCO...

            response = jsonify({"return_code": 200,
                                "message": "OK"
                                }), 200

        except:
            pass

    return response

@levels.route('/loadLevel', methods=['POST'])
def loadLevel():

    print("/loadLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data):

        try:
            
            level = Level.objects(id=data["id_level"]).get()

            name = level.name
            image = level.image
            blocked = level.blocked
            json = level.phaserObject
            # userName = level.username
            comments = level.comments
            

            # rate = 0 LevelRating.objects(id=data["id_level"]).get()
            avg = 0 # rate.avg

            response = jsonify({"return_code": 200,
                                "message": "OK",
                                "json": json,
                                "name_level": name,
                                "img": image,
                                # "id_user": userName, #PENDIENTE ISAURO
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

    # print("/storeLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("name_level" in data) and ("json" in data):
        
        # Genera ID único
        id = randint(0, max_level_id)

        try:

            Level(id=id, name=data["name_level"], phaserObject=data["json"]).save(force_insert=True)

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
    
    # print("/rateLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data) and ("id_user" in data) and ("rate" in data):
        
        try:

            # Actualiza la lista.            
            Level.objects(id=data["id_level"]).update_one(push__rating__ratingByUser=UserRating(username=data["id_user"], rating=data["rate"]))

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

            level.delete()

            response = jsonify({"return_code": 200, "message": "OK"}), 200

        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    return response
