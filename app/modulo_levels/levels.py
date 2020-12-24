from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoLevels import Level
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError
from random import randint

max_level_id = 999999999999

levels = Blueprint("levels", __name__)

@levels.route('/loadLevel', methods=['POST'])
def loadLevel():

    print("/loadLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data):
        try:
            json = Level.objects(id=data["id_level"]).get().phaserObject

            response = jsonify({"return_code": 200, "message": "OK", "json": json}), 200

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
            level = Level(id=id, name=data["name_level"], phaserObject=data["json"], rating=[], comments=[], blocked=False)

            level.save(force_insert=True)

            response = jsonify({"return_code": 200, "message": "OK", "id": id, "json": data["json"]}), 200
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
            level = Level.objects(id=data["id_level"]).get()
            Level.objects(id=data["id_level"]).update_one(push__comments=data[comment])
            # level.update_one(push__comments=data[comment]) # Si se puede asi, mejor

            level.reload()

            response = jsonify({"return_code": 200, "message": "OK"}), 200
        except:
            pass

    return response

# ESTA FUNCION MEJOR NO IMPLEMENTARLA HASTA QUE EN FRONTEND DECIDAN COMO QUIEREN LAS PUNTUACIONES
@levels.route('/rateLevel', methods=['PUT'])
def rateLevel():
    print("/rateLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data) and ("rate" in data):
        try:
            ### NO LO HAGAS TODAVIA LOCOOO

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
            level = Level.objects(id=data["id_level"]).get()

            level.delete()

            response = jsonify({"return_code": 200, "message": "OK"}), 200

        except:
            pass

    return response
