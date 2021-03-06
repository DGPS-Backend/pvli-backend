import functools
from flask import request, jsonify, Blueprint, session, g, redirect, url_for
from daos.daoUsers import User
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
from pymongo.errors import ServerSelectionTimeoutError
from flask_cors import CORS

users = Blueprint("users", __name__)

#Decorator function. It returns a new view function that wraps the original
# view it’s applied to. The new function checks if a user is loaded and
# redirects to the login page otherwise. If a user is loaded, the original
# view is called and continues normally.
def user_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            isRegularUser = True #TODO: Check if g.user is a regular user.

            if isRegularUser:
                return view(**kwargs)

        #By default, redirect to the login page if there is no user logged in.
        #redirect(url_for('TODO insert url for login page here'))
        return jsonify({"note": "this should redirect to the login page"}), 200

    return wrapped_view

CORS(users)
@users.route('/newUser', methods=['POST'])
def newUser():

    # print("/newUser RECIBE", request.get_json())

    data = request.get_json()
    response = jsonify({"return_code": 200, "message": "OK"}), 200

    if ("username" in data) and ("password" in data):

        try:
            User(username=data["username"], password=data["password"]).save(force_insert=True)
        except NotUniqueError:
            response = jsonify({"return_code": 601, "message": "User exists"}), 601
        except ValidationError:
            response = jsonify({"return_code": 400, "message": "Bad Request"}), 400
        except ServerSelectionTimeoutError:
            response = jsonify({"return_code": 500, "message": "Connection to database failed"}), 500

    else:

        response = jsonify({"return_code": 400, "message": "Bad Request"}), 400

    return response

# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
# OJO QUE LO MISMO HAY QUE HACER LA POLLA DE GOGLE
@users.route('/login', methods=['POST'])
def login():
    print("/login RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

# @users.before_app_request() registers a function that runs before the view function,
# no matter what URL is requested. load_logged_in_user checks if a user id is
# stored in the session and gets that user’s data from the database,
# storing it on g.user, which lasts for the length of the request.
# If there is no user id, or if the id doesn’t exist, g.user will be None.
@users.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = None #TODO: get the user with user_id from the database.
