from pymongo import MongoClient
from datetime import datetime

import serial
import serial.tools.list_ports
import time
import json


def obtener_bd(basedatos='memory_test',coleccion='data'):
    host = "192.168.0.100"
    port = "27017"
    cliente = MongoClient("mongodb://{}:{}".format(host, port))
    db = cliente[basedatos]
    collection = db[coleccion]
    return collection

def find_port(identf):
    """
        Esta función busca determinar el puerto serial que vamos a utilizar,
        se ingresa el identificador y si lo encuentra nos devuelve el nombre 
        del puerto al que esta conectado, de no ser así devuelve un 0. 
    """
    for port in serial.tools.list_ports.comports():
        if identf in str(port.hwid):
            return port.name

def insertar(time_string,tag,Antena,RSSI_1p,Azimuth_angle,Elevation_angle,Adv_Channel,Alt_ant):
    base_de_datos = obtener_bd()
    dato = base_de_datos
    return dato.insert_one({
        "hora": time_string,
        "Id_tag":tag,
        "Id_ant":Antena,
        "RSSI":RSSI_1p,
        "Ang_azimuth":Azimuth_angle,
        "Ang_elevacion":Elevation_angle,
        "Canal":Adv_Channel,
        "Altura_ant":Alt_ant
        }).inserted_id

def adquisicion_datos(iteraciones,Antena,Puerto,tag_1,tag_2,Alt_ant):
    print("Entre a la funcion")
    contador = 0
    tag_actual = ''

    # La hora
    time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

    while(contador<iteraciones):

        # Recolectando los datos
        line = Puerto.readline().decode('utf-8')

        if tag_1 in line:
            print("Entre al tag1")
            x1 = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p_1 = int(x1[1])
                Azimuth_angle_1 = int(x1[2])
                Elevation_angle_1 = int(x1[3])
                #RSSI_2p_1 = int(x1[4])
                Adv_Channel_1 = str(x1[5])
                Adv_Channel_1 = int(Adv_Channel_1)
                
                if(tag_actual!=tag_1):
                    print("Dato recibido correctamente")
                    #print("RSSI:",RSSI_1p_1," ,A_a:",Azimuth_angle_1," ,A_e:",Elevation_angle_1," ,Canal",Adv_Channel_1, " ,Antena:",Antena," ,tag:",tag_1)
                    insertar(time_string,tag_1,Antena,RSSI_1p_1,Azimuth_angle_1,Elevation_angle_1,Adv_Channel_1,Alt_ant)
                    #enviar_php_datos_ant(time_string,tag_1,Antena,RSSI_1p_1,Azimuth_angle_1,Elevation_angle_1,Adv_Channel_1,Alt_ant)
                    #time.sleep(0.1)
                    contador = contador + 1
                    print(contador)
                    tag_actual = tag_1
            except: 
                pass  

        elif tag_2 in line:
            print("Entre al tag2")
            x2 = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p_2 = int(x2[1])
                Azimuth_angle_2 = int(x2[2])
                Elevation_angle_2 = int(x2[3])
                #RSSI_2p_2 = int(x2[4])
                Adv_Channel_2 = str(x2[5])
                Adv_Channel_2 = int(Adv_Channel_2)
                
                if(tag_actual!=tag_2):
                    print("Dato recibido correctamente")
                    #print("RSSI:",RSSI_1p_2," ,A_a:",Azimuth_angle_2," ,A_e:",Elevation_angle_2," ,Canal",Adv_Channel_2, " ,Antena:",Antena," ,tag:",tag_2)
                    #enviar_php_datos_ant(time_string,tag_2,Antena,RSSI_1p_2,Azimuth_angle_2,Elevation_angle_2,Adv_Channel_2,Alt_ant)
                    insertar(time_string,tag_2,Antena,RSSI_1p_2,Azimuth_angle_2,Elevation_angle_2,Adv_Channel_2,Alt_ant)
                    #time.sleep(0.1)
                    contador = contador + 1
                    print(contador)
                    tag_actual = tag_2
            except: 
                pass  
        
        else:
            print("Dato recibido de forma incorrecta")



# Inicializando las variables
Altura_ant = 170        ## Esta debe estar en cm
segundo_actual = datetime.today().second
segundo_siguiente = segundo_actual + 1

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
U_Blox = serial.Serial(str(find_port(ant_conexion)),115200) # en windows
print(U_Blox)

try:
    while True:
        #print("Entre al while exterior")
        segundo_actual = datetime.today().second

        if segundo_actual == segundo_siguiente:
            
            segundo_siguiente = segundo_siguiente + 1
            #print("Entre al if exterior")
            if segundo_siguiente == 60 :
                segundo_siguiente = 0
            adquisicion_datos(4,ant_dato,U_Blox,tag_1,tag_2,Altura_ant)
            print(segundo_actual)
            print(segundo_siguiente)
            
        
except KeyboardInterrupt:
    print("El usuario a detenido el programa")
    U_Blox.close()

except serial.SerialException:
    print("Error en la conexión con el programa")    


