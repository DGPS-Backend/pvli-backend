from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoLevels import Level
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError

levels = Blueprint("levels", __name__)

@levels.route('/loadLevel', methods=['POST'])
def loadLevel():

    print("/loadLevel RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    if ("id_level" in data):
        try:
            json = Level.objects(id_level=data["id_level"]).get().json_phaser

            response = jsonify({"return_code": 200, "message": "OK", "json": json}), 200

        except:
            pass

    return response

@levels.route('/storeLevel', methods=['POST'])
def storeLevel():
    print("/storeLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@levels.route('/commentLevel', methods=['PUT'])
def commentLevel():
    print("/commentLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@levels.route('/rateLevel', methods=['PUT'])
def rateLevel():
    print("/rateLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@levels.route('/eraseLevel', methods=['POST'])
def eraseLevel():
    print("/eraseLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200
