import pymongo
import servidor_mongo as SM
import time

## Una variable importante que de no estar almacenada debe darse de igual manera es la distancia entre la antena y el tag -> debería ser un dato almacenado
## Voy a tratar de corregir eso mañana
D_ant_tag = 130 
## Debe estar en centimetros
## Establecemos la conexion con el servidor
base_de_datos = SM.obtener_bd()

# Definimos una variable con los atributos de un elemento almacenado por primera vez
final_data = SM.Ublox_1

#respuesta = base_de_datos.datos.find_one()

time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
time.sleep(1)
time_string2 = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

print(time_string)
print(time_string2)


