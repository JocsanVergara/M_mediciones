# Instalación de dependencias
#python -m pip install pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

def obtener_bd():
    host = "localhost"
    puerto = "27017"
    user = ""
    password = ""
    database = "memory_test"
    colection = "data"
    cliente = MongoClient("mongodb://{}:{}@{}:{}".format(user, password, host, puerto))
    return cliente[database]

def insertar(dato):
    base_de_datos = obtener_bd()
    dato = base_de_datos.data
    return dato.insert_one({
        "nombre": dato.nombre,
        "precio": dato.precio,
        "cantidad": dato.cantidad,
        }).inserted_id

def obtener():
    base_de_datos = obtener_bd()
    return base_de_datos.datos.find()

def actualizar(id, dato):
    base_de_datos = obtener_bd()
    resultado = base_de_datos.dato.update_one(
        {
        '_id': ObjectId(id)
        }, 
        {
            '$set': {
                "nombre": dato.nombre,
                "precio": dato.precio,
                "cantidad": dato.cantidad,
            }
        })
    return resultado.modified_count

def eliminar(id):
    base_de_datos = obtener_bd()
    resultado = base_de_datos.dato.delete_one(
        {
        '_id': ObjectId(id)
        })
    return resultado.deleted_count

