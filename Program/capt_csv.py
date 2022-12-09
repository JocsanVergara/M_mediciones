import argparse

from datetime import datetime, timedelta
import json
import serial
import serial.tools.list_ports
import pandas as pd
import time

# Funciones
def find_port(identf):
    """
        Esta función busca determinar el puerto serial que vamos a utilizar,
        se ingresa el identificador y si lo encuentra nos devuelve el nombre 
        del puerto al que esta conectado, de no ser así devuelve un 0. 
    """
    for port in serial.tools.list_ports.comports():
        if identf in str(port.hwid):
            return port.name

## Para entregarle los argumento desde linea de comando
parser = argparse.ArgumentParser()
parser.add_argument("Punto_captura",type=int,help="Corresponde al punto donde fue tomada la muestra")
parser.add_argument("Altura_antena",type=int,help="Altura de la antena que estamos recogiendo el dato")
parser.add_argument("Distancia_entre_antenas",type=int,help="Distancia lineal entre ambas antenas")
parser.add_argument("Error_dato",type=int,help="Existe libre vision entre el objetivo y la antena,")
parser.add_argument("Distancia_ant_tag",type=int,help="Distancia lineal entre la antena y el tag")
args = parser.parse_args()

## Control de los dos minutos de captura de datos
time2 = datetime.now() + timedelta(minutes=1)
#time2 = datetime.now() + timedelta(seconds=10)

## Conexion con las antenas
# Leemos el json con los datos de las antenas y el tag
f = open("Ant_tag.json", "r")
c = f.read()
f.close()
js = json.loads(c)

ant_conexion = js["Ant_ubuntu"]
ant_dato = js["Antena_1"]
#ant_conexion = ant_dato   # en Windows nos pide el identificador de la antena
tag_1 = js["tag_1"]
tag_2 = js["tag_2"]
tag = tag_1

# Estableciendo la conexion con el puerto Serial de la antena
U_Blox = serial.Serial(ant_conexion,115200)
#U_Blox = serial.Serial(str(find_port(ant_conexion)),115200) # en windows
time_string1 = time.strftime("%Y%m%d_%H%M%S",time.localtime())
print(time_string1)

lista_datos = []
contador = 0
while(True):
    time1 = datetime.now()
    if(time1.minute == time2.minute):
        if(time1.second == time2.second): 
            break
    #print("Prueba correctamente ejecutada")
    # La hora
    time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
    try:
        # Recolectando los datos
        line = U_Blox.readline().decode('utf-8')
        #print(line)
        if tag in line:
            x = line.split(",")
            try:
                Identificador = str(x[0])
                RSSI_1p = int(x[1])
                Azimuth_angle = int(x[2])
                Elevation_angle = int(x[3])
                #RSSI_2p = int(x[4])
                Adv_Channel = str(x[5])
                try:
                    Adv_Channel = int(Adv_Channel)
                except:
                    Adv_Channel = 38
                contador = contador + 1
                print("Dato {:} recibido correctamente".format(contador))
                lista_datos.append({'hora':time_string,
                            'Id_tag': tag,
                            'Id_Ant':ant_dato,
                            'RSSI':RSSI_1p,
                            'Ang_azimuth':Azimuth_angle,
                            'Ang_elevacion':Elevation_angle,
                            'Canal':Adv_Channel,
                            'Altura_ant(cm)': args.Altura_antena,
                            'Distancia_entre_ant_tag(cm)': args.Distancia_ant_tag,
                            'Error_dato_medido': args.Error_dato,
                            'Distancia_entre_ant':args.Distancia_entre_antenas})
            except:
                pass
    except KeyboardInterrupt:
        print("El usuario a detenido el programa")
        U_Blox.close()

    except serial.SerialException:
        print("Error en la conexión con el programa")  

df = pd.DataFrame(lista_datos)

## Archivo
archivo = time_string1 + '_' + str(args.Altura_antena) + '_' + str(args.Distancia_ant_tag) + '_' + str(args.Error_dato) + '.csv'
df.to_csv(archivo,encoding = 'utf-8')