from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoLevels import Level, LevelRating
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
            json = level.phaserObject
            name = level.name
            image = level.image
            userName = level.userName
            comments = level.comments
            blocked = level.blocked

            rate = LevelRating.objects(id=data["id_level"]).get()
            avg = rate.avg

            response = jsonify({"return_code": 200,
                                "message": "OK",
                                "json": json,
                                "name_level": name,
                                "img": image,
                                "id_user": userName, #PENDIENTE ISAURO
                                "comments": comments, #TODO
                                "blocked": blocked, #PENDIENTE ISAURO
                                "rate": avg,
                                }), 200

        except:
            pass

    return response

@levels.route('/storeLevel', methods=['POST'])
def storeLevel():

    print("/storeLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("name_level" in data) and ("json" in data):
        # Genera ID único
        id = randint(0, max_level_id)

        try:
            # TODO EL COMENTS ARREGLAR BIEN EN EL DAO DE LA POLLA
            Level(id=id, name=data["name_level"], phaserObject=data["json"], comments=[""], blocked=False).save(force_insert=True)
            LevelRating(id=id, avg=0.0, ratingByUser=[0]).save(force_insert=True)

            response = jsonify({"return_code": 200,
                                "message": "OK",
                                "id": id,
                                "json": data["json"]
                                }), 200
        except:
            pass

    return response

@levels.route('/commentLevel', methods=['PUT'])
def commentLevel():

    print("/commentLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data) and ("comment" in data):
        try:
            level = Level.objects(id=data["id_level"])
            # TODO ADAPTAR AL FORMATO DE COMENTARIO TOCHO DE LOS GUEVOS
            level.update_one(push__comments=data["comment"])
            # level.reload()

            response = jsonify({"return_code": 200, "message": "OK"}), 200
        except:
            pass

    return response

@levels.route('/rateLevel', methods=['PUT'])
def rateLevel():
    print("/rateLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data) and ("rate" in data):
        try:
            rate = LevelRating.objects(id=data["id_level"])
            # TODO ADAPTAR AL FORMATO DE PUNTUACION TOCHO DE LOS GUEVOS
            # Seria insertar mas calcular la media
            rate.update_one(push__ratingByUser=data["rate"])

            response = jsonify({"return_code": 200, "message": "OK"}), 200
        except:
            pass

    return response

@levels.route('/eraseLevel', methods=['POST'])
def eraseLevel():

    print("/eraseLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data):
        try:
            level = Level.objects(id=data["id_level"])

            level.delete()

            response = jsonify({"return_code": 200, "message": "OK"}), 200

        except:
            pass

    return response
