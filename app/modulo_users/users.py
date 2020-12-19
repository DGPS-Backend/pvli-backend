from flask import request
from flask import jsonify
from flask import Blueprint
from daos.daoUsers import Usuarios
from mongoengine.errors import NotUniqueError

users = Blueprint("users", __name__)

@users.route('/newUser', methods=['POST'])
def newUser():
    
    data = request.get_json() 
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("username" in data) and ("password" in data):    
        
        try:
            Usuarios(username=data["username"], password=data["password"]).save(force_insert=True)
        except NotUniqueError:
            response = jsonify({"return_code": 601, "message": 'El usuario ya existía'}), 601

    else:

        response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    return response

@users.route('/login', methods=['POST'])
def login():
    print("/login RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200