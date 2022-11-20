# Instalación de dependencias
#python -m pip install pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId

class Ublox_1:
    def __init__(self, hora,Id_tag,Id_ant,RSSI,Ang_elevacion,Canal,Altura_ant):
        self.hora = hora
        self.Id_tag = Id_tag
        self.Id_ant = Id_ant
        self.RSSI = RSSI
        self.Ang_elevacion = Ang_elevacion
        self.Canal = Canal
        self.Altura_ant = Altura_ant

class Ublox_2:
    def __init__(self,Distancia_ant_tag,LOS,Distancia_corregida,Latitud,Longitud,Dato_completo):
        self.Distancia_ant_tag = Distancia_ant_tag
        self.LOS = LOS
        self.Distancia_corregida = Distancia_corregida
        self.Latitud = Latitud
        self.Longitud = Longitud
        self.Dato_completo = Dato_completo    

class Ublox_3:
    def __init__(self,hora,Id_tag,Id_ant,RSSI,Ang_elevacion,Canal,Altura_ant,Distancia_ant_tag,LOS,Distancia_corregida,Latitud,Longitud,Dato_completo):
        self.hora = hora
        self.Id_tag = Id_tag
        self.Id_ant = Id_ant
        self.RSSI = RSSI
        self.Ang_elevacion = Ang_elevacion
        self.Canal = Canal
        self.Altura_ant = Altura_ant
        self.Distancia_ant_tag = Distancia_ant_tag
        self.LOS = LOS
        self.Distancia_corregida = Distancia_corregida
        self.Latitud = Latitud
        self.Longitud = Longitud
        self.Dato_completo = Dato_completo

def obtener_bd(basedatos='memory_test',coleccion='products'):
    host = "localhost"
    port = "27017"
    cliente = MongoClient("mongodb://{}:{}".format(host, port))
    db = cliente[basedatos]
    collection = db[coleccion]
    return collection

def obtener_bd_1():
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

