import pymongo
import servidor_mongo as SM
import json
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import utils

## Nota: Una variable importante que de no estar almacenada debe darse de igual manera es la distancia entre la antena y el tag -> debería ser un dato almacenado

## Debe estar en centimetros
D_ant_tag = 130 

## Leemos el json con los datos de las antenas y el tag
f = open("Ant_tag.json", "r")
c = f.read()
f.close()
js = json.loads(c)

## Establecemos la conexion con el servidor
base_de_datos = SM.obtener_bd()

# Definimos una variable con los atributos de un elemento almacenado por primera vez
# final_data = SM.Ublox_1

## Pruebas de código ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# fecha = datetime.strptime("2022/11/17/ 21:42:28","%Y/%m/%d/ %H:%M:%S")
# print(fecha,type(fecha))
# fecha_str = str(fecha)
# print(fecha_str,type(fecha_str))
# time_0 = '2022/11/17/ 21:42:28'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Traemos el ultimo elemento de la lista en el tiempo de lectura
## La idea es poder trabajar con el tiempo anterior a este número
r_0 = base_de_datos.find().sort("_id",-1).limit(1)

for r in r_0:
    id_0 = r

fecha_0 = str(datetime.strptime(str(id_0['hora']),"%Y/%m/%d/ %H:%M:%S"))

time_1 = datetime.strptime(str(id_0['hora']),"%Y/%m/%d/ %H:%M:%S") - timedelta(seconds=1)
fecha_1 = str(time_1)

time_2 = datetime.strptime(str(id_0['hora']),"%Y/%m/%d/ %H:%M:%S") - timedelta(seconds=2)
fecha_2 = str(time_2)

time_3 = datetime.strptime(str(id_0['hora']),"%Y/%m/%d/ %H:%M:%S") - timedelta(seconds=3)
fecha_3 = str(time_3)

time_4 = datetime.strptime(str(id_0['hora']),"%Y/%m/%d/ %H:%M:%S") - timedelta(seconds=4)
fecha_4 = str(time_4)
# Nota: Esto se puede reducir más todavia pero quiero saber si funciona todo primero antes de meterle mano a todo

## Traigo una cantidad de datos desde la base de datos, está a su vez esta limitado con la variable contenida en la clase limit()
## Lo separo en 4 vectores porque no tengo garantía de que todos los datos hayan sido recibidos en orden y con la misma hora
## Existe la posibilidad de que los datos se pierdan en el camino, que la antena deje de mandar datos, que las baterias de los tag se agoten y dejen de enviar datos, que el trafico de red sea demasiado para el ordenador que hace de host del servidor o que el mismo repetidor que ocupo no sea capaz de procesar las instrucciones aunque lo dudo, pero en retrospectiva puede pasar, podría ser victima de un ataque de Ddos

respuestas = base_de_datos.find().sort("_id",-1)#.limit(500)

# tag_1/Ant_1
vect_11 = []
# tag_2/Ant_1
vect_21 = []
# tag_1/Ant_2
vect_12 = []
# tag_2/Ant_2
vect_22 = []

for r in respuestas:
    if(r['Id_tag']== js["tag_1"] and r['Id_ant']==js["Antena_1"]):
        vect_11.append(r)
    elif(r['Id_tag']== js["tag_2"] and r['Id_ant']==js["Antena_1"]):
        vect_21.append(r)
    elif(r['Id_tag']== js["tag_1"] and r['Id_ant']==js["Antena_2"]):
        vect_12.append(r)
    elif(r['Id_tag']== js["tag_2"] and r['Id_ant']==js["Antena_2"]):
        vect_22.append(r)
    else:
        pass

## De los cuatro vector que creamos, los reducimos a dos para poder tener las variables que tienen el mismo tag con antenas diferentes
## El críterio para juntar alguno de los elementos es que tengan la misma hora de captura del dato y que el tag sea igual en ambos casos pero los datos deben ser tomado de diferentes antenas
## En este caso tenemos solo dos antenas y dos tag

vect_1 = []
vect_2 = []
# cargamos los datos al vect_1
for r in vect_11:
    #print(r['hora'])
    for s in vect_12:
        #print(s['hora'])
        #print("~"*50)
        if(r['hora']==s['hora']):
            #print("3")
            vect_1.append(r)
            vect_1.append(s)
            vect_12.remove(s)

# Cargamos los datos al vect_2
for r in vect_21:
    #print("1")
    for s in vect_22:
        #print("2")
        if(r['hora']==s['hora']):
            #print("3")
            vect_2.append(r)
            vect_2.append(s)
            vect_22.remove(s)

## Testeo de variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print("~"*50)
# print(vect_1[0])
# print(vect_1[1])
# print("~"*50)
# print(vect_2[0])
# print(vect_2[1])
# print(vect_1[0]['_id'])
# print(ObjectId(str(vect_1[0]['_id'])))
# # print(vect_1[2])
# # print(vect_1[3])
# # print(vect_1[4])
# # print(vect_1[5])
# print("~"*50)
# print(len(vect_1))
# print(len(vect_2))
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Para ingresar a los elementos del arreglo y modificarlos
## Actualizo los datos añadiendo el parametro Distancia_ant_tag para guardarlos en la base de datos de MongoDb
## Vector 1
for t in range(int(len(vect_1)/2)):
    print("~"*50)
    D_B,D_A = utils.Distancia_ant_tag(D_ant_tag,vect_1[2*t]['Ang_azimuth'],vect_1[(2*t)+1]['Ang_azimuth'])
    d_a = D_A
    d_b = D_B
    base_de_datos.update_one(
        {"_id": ObjectId(str(vect_1[2*t]['_id']))},
        {
            "$set":{
                "Distancia_ant_tag": d_b
            }
        }
    )

    base_de_datos.update_one(
        {"_id": ObjectId(vect_1[(2*t)+1]['_id'])},
        {
            "$set":{
                "Distancia_ant_tag": d_a
            }
        }
    )

## Vector 2
for t in range(int(len(vect_2)/2)):
    print("~"*50)
    D_B,D_A = utils.Distancia_ant_tag(D_ant_tag,vect_2[2*t]['Ang_azimuth'],vect_2[(2*t)+1]['Ang_azimuth'])
    
    base_de_datos.update_one(
        {'_id': ObjectId(vect_2[2*t]['_id'])},
        {
            '$set':{
                "Distancia_ant_tag": D_B
            }
                
        }
    )
    base_de_datos.update_one(
        {'_id': ObjectId(vect_2[(2*t)+1]['_id'])},
        {
            '$set':{
                "Distancia_ant_tag": D_A
            }
        }
    )

# Nota esto podría ser una función pero de momento lo tengo todo junto no más


 #utils.Act_D_ant_tag(base_de_datos,vect_2[2*t]['_id'],D_B)
#utils.Act_D_ant_tag(base_de_datos,vect_2[(2*t)+1]['_id'],D_A)
