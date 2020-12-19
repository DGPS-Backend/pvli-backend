from flask import request
from flask import jsonify
from flask import Blueprint

admin = Blueprint("admin", __name__)

@admin.route('/getStatistics', methods=['GET'])
def getStatistics():
    print("/getStatistics RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@admin.route('/getAdminData', methods=['GET'])
def getAdminData():
    print("/getAdminData RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@admin.route('/blockLevel', methods=['PUT'])
def blockLevel():
    print("/blockLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@admin.route('/unblockLevel', methods=['PUT'])
def unblockLevel():
    print("/unblockLevel RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@admin.route('/blockUser', methods=['PUT'])
def blockUser():
    print("/blockUser RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200

@admin.route('/unblockUser', methods=['PUT'])
def unblockUser():
    print("/unblockUser RECIBE", request.get_json())
    return jsonify({"return_code": "200"}), 200
