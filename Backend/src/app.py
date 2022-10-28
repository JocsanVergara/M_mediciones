# Dependencias necesarias para correr este programa
# pip install flask Flask-Pymongo flask-cors

# Llamada de dependencias
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

# Conexión con el servidor de mongo, la base de datos ServerMemory   :27017
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ServerMemory'
mongo = PyMongo(app)

# para evitar conflictos con el servidor de REACT usamos CORS
# Estas son una serie de reglas que ambos servidores deben cumplir para no tener problemas n.n
CORS(app)

# Ahora voy a conectarme a la colección users
db = mongo.db.users

# Es necesario escribir rutas
@app.route('/')
def index():
    return '<h1>HELLO WORLD</h1>'

# Creamos un documento de JSON con los datos entregados por la página en la base de datos
@app.route('/users', methods = ['POST'])
def createUser():
    id = db.insert_one({
        'name' : request.json['name'],
        'email' : request.json['email'],
        'password': request.json['password']
    }).inserted_id
    print(str(ObjectId(id)))
    return jsonify(str(ObjectId(id)))

# Listar los archivos en la base de datos
@app.route('/users',methods = ['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id' : str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'email':doc['email'],
            'password':doc['password']
        })
    return jsonify(users)

# Listar un solo documento con el respectivo id
@app.route('/user/<id>',methods = ['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name':user['name'],
        'email':user['email'],
        'password':user['password']
    })

@app.route('/users/<id>',methods = ['DELETE'])
def deleteUser(id):
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({'msg':'Usuario eliminado'})

@app.route('/users/<id>',methods = ['PUT'])
def updateUser(id):
    db.update_one({
        {'_id': ObjectId(id)},
        {
            'name': request.json['name'],
            'email':request.json['email'],
            'password':request.json['password']
        }
    })
    return jsonify({'msg':'Se han actualizado los datos del usuario'})

if __name__ == '__main__':
    app.run(debug = True)