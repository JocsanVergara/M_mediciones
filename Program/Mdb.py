import pymongo
import servidor_mongo as SM
import time
import json
from bson.objectid import ObjectId
from datetime import datetime
from pathlib import Path
import utils

## Una variable importante que de no estar almacenada debe darse de igual manera es la distancia entre la antena y el tag -> debería ser un dato almacenado
## Voy a tratar de corregir eso mañana
D_ant_tag = 130 

# Leemos el json con los datos de las antenas y el tag


f = open("Ant_tag.json", "r")
c = f.read()
f.close()
js = json.loads(c)

## Debe estar en centimetros
## Establecemos la conexion con el servidor
base_de_datos = SM.obtener_bd()

# Definimos una variable con los atributos de un elemento almacenado por primera vez
final_data = SM.Ublox_1

fecha = datetime.strptime("2022/11/17/ 21:42:28","%Y/%m/%d/ %H:%M:%S")
print(fecha,type(fecha))
fecha_str = str(fecha)
print(fecha_str,type(fecha_str))
time_0 = '2022/11/17/ 21:42:28'

# Traemos el ultimo elemento de la lista en el tiempo de lectura
r_0 = base_de_datos.find().sort("_id",-1).limit(1)

for r in r_0:
    id_0 = r


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

vect_1 = []
vect_2 = []

## necesitamos revisar cuales son iguales
for r in vect_11:
    print(r['hora'])
    for s in vect_12:
        print(s['hora'])
        print("~"*50)
        if(r['hora']==s['hora']):
            print("3")
            vect_1.append(r)
            vect_1.append(s)
            vect_12.remove(s)

for r in vect_21:
    print("1")
    for s in vect_22:
        print("2")
        if(r['hora']==s['hora']):
            print("3")
            vect_2.append(r)
            vect_2.append(s)
            vect_22.remove(s)

print("~"*50)
print(vect_1[0])
print(vect_1[1])
print("~"*50)
print(vect_2[0])
print(vect_2[1])
print(vect_1[0]['_id'])
print(ObjectId(str(vect_1[0]['_id'])))
# print(vect_1[2])
# print(vect_1[3])
# print(vect_1[4])
# print(vect_1[5])
print("~"*50)
print(len(vect_1))
print(len(vect_2))

# Para ingresar a los elementos del arreglo y modificarlos

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
    #utils.Act_D_ant_tag(base_de_datos,vect_2[2*t]['_id'],D_B)
    #utils.Act_D_ant_tag(base_de_datos,vect_2[(2*t)+1]['_id'],D_A)
