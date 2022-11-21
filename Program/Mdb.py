import pymongo
import servidor_mongo as SM
import time

from bson.objectid import ObjectId

## Una variable importante que de no estar almacenada debe darse de igual manera es la distancia entre la antena y el tag -> debería ser un dato almacenado
## Voy a tratar de corregir eso mañana
D_ant_tag = 130 

## Debe estar en centimetros
## Establecemos la conexion con el servidor
base_de_datos = SM.obtener_bd()

# Definimos una variable con los atributos de un elemento almacenado por primera vez
final_data = SM.Ublox_1

#respuesta = base_de_datos.datos.find_one()

time_0 = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
time.sleep(1)
time_1 = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
time.sleep(1)
time_2 = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
time.sleep(1)
time_3 = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

# Traemos el ultimo elemento de la lista en el tiempo de lectura
r_0 = base_de_datos.find(
    {
        "hora" : time_0
    }
).sort({"_id":1})

id_0 = r_0['_id']

respuestas = base_de_datos.find(
    {
        "_id" : {
            '$lte' :ObjectId(r_0['_id'])
        }
            
    }
)

lr = []
for r in respuestas:
    lr.append[r]


