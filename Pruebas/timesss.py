#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
from twisted.internet import reactor
import serial
import json 
import utils

time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

# Inicializando las variables
Altura_ant = 134        ## Esta debe estar en cm

# Leemos el json con los datos de las antenas y el tag
f = open("Ant_tag.json", "r")
c = f.read()
f.close()

js = json.loads(c)
#ant_conexion = js["Ant_ubuntu"]
ant_dato = js["Antena_2"]
ant_conexion = ant_dato   # en Windows nos pide el identificador de la antena
tag_1 = js["tag_1"]
tag_2 = js["tag_2"]

# Estableciendo la conexion con el puerto Serial de la antena
#U_Blox = serial.Serial(ant_conexion,115200)
U_Blox = serial.Serial(str(utils.find_port(ant_conexion)),115200) # en windows
print(U_Blox)

def func1(x):
    print(50*'~')
    print(x)
    #time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
    #print(time_string)
    try:
        utils.adquisicion_datos(4,ant_dato,U_Blox,tag_1,tag_2,Altura_ant)
        print(time_string)
    except KeyboardInterrupt:
        print("El usuario a detenido el programa")
        U_Blox.close()

    except serial.SerialException:
        print("Error en la conexión con el programa")  

    # indicamos nuevamente que llame a la funcion func1...
    reactor.callLater(1, func1, "se esta ejecutando cada segundo")
 
# indicamos que cada segundos, llame a la funcion func1 y le pase como
# parametro "inicio"
reactor.callLater(1, func1, "inicio")
reactor.run()

