# *** Librerías del server ***
from flask import Flask
from flask import jsonify
from flask_mongoengine import MongoEngine

# *** Blueprints (Módulos) ***
from modulo_users.users import users
from modulo_admin.admin import admin
from modulo_levels.levels import levels

# *** Aplicación y módulos ***
app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(levels)

# *** Base de datos ***
app.config['MONGODB_SETTINGS'] = {
    'db': 'game',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)

# *** Prueba para saber si el servidor responde ***
@app.route('/prueba', methods=['GET','POST','PUT','DELETE'])
def prueba():
    return jsonify({"return_code": "200"}), 200

# *** La petición solicitada no se ha encontrado ***
@app.errorhandler(404)
def err404(error):
    return jsonify({"return_code": "404"}), 404

# *** La petición es correcta, pero el método de invocación no ***
@app.errorhandler(405)
def err405(error):
    return jsonify({"return_code": "405"}), 405

# *** Error interno en el servidor ***
@app.errorhandler(500)
def err500(error):
    return jsonify({"return_code": "500"}), 500

if __name__ == "__main__":

    app.run(host='127.0.0.1', port=8080, debug=True)
