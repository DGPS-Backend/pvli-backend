import functools
from flask import request, jsonify, Blueprint, session, g, redirect, url_for
from daos.daoLevels import Level
from daos.daoUsers import User
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError

admin = Blueprint("admin", __name__)

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            isAdminUser = True #TODO: Check if g.user is an administrator.

            if isAdminUser:
                return view(**kwargs)

        #By default, redirect to the login page if there is no admin logged in.
        #redirect(url_for('TODO insert url for login page here'))
        return jsonify({"note": "this should redirect to the login page"}), 200

    return wrapped_view

@admin.route('/getStatistics', methods=['GET'])
#@admin_required TODO uncomment for release.
def getStatistics():
    #receivedData = request.get_json()
    dataToSend = "No statistics."

    #TODO get the statistics into dataToSend.

    return jsonify({"return_code": "200", "data": dataToSend}), 200

@admin.route('/getAdminData', methods=['GET'])
def getAdminData():
    #print("/getAdminData RECIBE", request.get_json())
    try:
        levels = Level.objects()
        users = User.objects()
        response = jsonify({"return_code": "200", "users":users.to_json(), "levels":levels.to_json()}), 200
    except :
        response = jsonify({"return_code": "500","message": "Internal Problem"}), 500

    return response


@admin.route('/blockLevel', methods=['PUT'])
def blockLevel():
    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("id_level" in data):
        try:
            level = Level.objects(id=data["id_level"])
            levelInfo = level.get()
            if not levelInfo.blocked :
                level.update_one(blocked=True)
                mssg = "the level: {} is now blocked".format(levelInfo.id)
            else :
                mssg = "the level: {} was already blocked".format(levelInfo.id)

            response = jsonify({"return_code": 200, "message": mssg}), 200
        except :
            response = jsonify({"return_code": 200, "message": "The level can't be blocked"}), 601

    else:

        response = jsonify({"return_code": 400, "message": "Wrong Solicitation"}), 400

    return response

@admin.route('/unblockLevel', methods=['PUT'])
def unblockLevel():
    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("id_level" in data):
        try:
            level = Level.objects(id=data["id_level"])
            levelInfo = level.get()
            if levelInfo.blocked :
                level.update_one(blocked=False)
                mssg = "the level: {} is now not blocked".format(levelInfo.id)
            else :
                mssg = "the level: {} was already not blocked".format(levelInfo.id)

            response = jsonify({"return_code": 200, "message": mssg}), 200
        except :
            response = jsonify({"return_code": 200, "message": "The level can't be unblocked"}), 601

    else:

        response = jsonify({"return_code": 400, "message": "Wrong Solicitation"}), 400

    return response

@admin.route('/blockUser', methods=['PUT'])
def blockUser():

    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("username" in data):
        try:
            user = User.objects(username=data["username"])
            userInfo = user.get()
            if userInfo.blocked :
                mssg = "the user: {} was already blocked".format(userInfo.username)
            else :
                user.update_one(blocked=True)
                mssg = "the user: {} is now blocked".format(userInfo.username)

            response = jsonify({"return_code": 200, "message": mssg}), 200
        except :
            response = jsonify({"return_code": 200, "message": "The user can`t be blocked"}), 601

    else:

        response = jsonify({"return_code": 400, "message": "Wrong Solicitation"}), 400

    return response

@admin.route('/unblockUser', methods=['PUT'])
def unblockUser():

    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("username" in data):
        try:
            user = User.objects(username=data["username"])
            userInfo = user.get()
            if userInfo.blocked :
                user.update_one(blocked=False)
                mssg = "the user: {} is now not blocked".format(userInfo.username)
            else :
                mssg = "the user: {} was already not blocked".format(userInfo.username)

            response = jsonify({"return_code": 200, "message": mssg}), 200
        except :
            response = jsonify({"return_code": 200, "message": "The user can`t be unblocked"}), 601

    else:

        response = jsonify({"return_code": 400, "message": "Wrong Solicitation"}), 400

    return response

@admin.route('/getUserInfo', methods=['GET'])
def getUserInfo():

    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("username" in data):
        try:
            user = User.objects(username=data["username"]).get()
            response = jsonify({"return_code": 200, "message": user}), 200
        except :
            response = jsonify({"return_code": 500, "message": "No se pueden obtener los datos de los usuarios"}), 400
    else:

        response = jsonify({"return_code": 400, "message": "Solicitud incorrecta"}), 400

    return response

# @admin.before_app_request() registers a function that runs before the view function,
# no matter what URL is requested. load_logged_in_user checks if a user id is
# stored in the session and gets that user’s data from the database,
# storing it on g.user, which lasts for the length of the request.
# If there is no user id, or if the id doesn’t exist, g.user will be None.
@admin.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = None #TODO: get the user with user_id from the database.