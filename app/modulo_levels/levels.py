from flask import request
from flask import jsonify
from flask import Blueprint

levels = Blueprint("levels", __name__)

@levels.route('/loadLevel', methods=['POST'])
def loadLevel():
    print("/loadLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

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
