import serial
import serial.tools.list_ports
import os
import csv
import pathlib
import time

def find_port(identf):
    """
        Esta función busca determinar el puerto serial que vamos a utilizar,
        se ingresa el identificador y si lo encuentra nos devuelve el nombre 
        del puerto al que esta conectado, de no ser así devuelve un 0. 
    """
    for port in serial.tools.list_ports.comports():
        if identf in str(port.hwid):
            return port.name

def adquisicion_datos(nombre_archivo,iteraciones,Puerto,tag,campo_vision,altura_ant,dxy_en_cm,dz_en_cm):
    #cantidad = iteraciones                              #No es necesaria pero podría darse el caso de que yo determine el número de iteraciones que quiero usar y me sería más facil cambiar un valor en la función directamente
    campos = ['Hora','Antena','iden.Tag','RSSI_1','Ang.Azimuth','Ang.Elevacion','RSSI_2','Canal','Linea de visión libre(si=1, no=0)','altura de la antena, respecto del nivel del suelo','Distancia entre antena con el tag en cm','Distancia entre el suelo con el tag en cm']

    if not pathlib.Path(nombre_archivo).exists():
        with open(nombre_archivo,'w',newline='') as archivo_csv:
            write = csv.DictWriter(archivo_csv,fieldnames=campos)
            write.writeheader()

    with open(nombre_archivo,'a',newline='') as archivo_csv:
        write = csv.DictWriter(archivo_csv,fieldnames=campos)    #En el formato anterior usaba el ; para que los valores pasaran a otra linea
        contador = 0

        while(contador<iteraciones):
            os.system('cls')
            print("Guardando dato número: ",contador)
            
            time.sleep(0.2)

            #La hora
            time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())
            
            #Recolectando los datos
            line = Puerto.readline().decode('utf-8')
            print(line)
            if tag in line:
                x = line.split(",")
                try: 
                    Identificador = str(x[0])
                    RSSI_1p = int(x[1])
                    Azimuth_angle = int(x[2])
                    Elevation_angle = int(x[3])
                    RSSI_2p = int(x[4])
                    Adv_Channel = str(x[5])
                    print("Dato recibido correctamente")
                    write.writerow({'Hora':time_string,
                                'Antena':Identificador,
                                'iden.Tag': tag,
                                'RSSI_1':RSSI_1p,
                                'Ang.Azimuth':Azimuth_angle,
                                'Ang.Elevacion':Elevation_angle,
                                'RSSI_2':RSSI_2p,
                                'Canal':Adv_Channel,
                                'Linea de visión libre(si=1, no=0)':campo_vision,
                                'altura de la antena, respecto del nivel del suelo': altura_ant,
                                'Distancia entre antena con el tag en cm': dxy_en_cm,
                                'Distancia entre el suelo con el tag en cm': dz_en_cm})
                    contador = contador + 1    
                except: 
                    pass     
            else:
                print("Dato recibido de forma incorrecta")

cte_conv = 2*60            
n =  cte_conv * 5 #Numero de iteraciones por minutos de captura (5min)
#Nombre de las antenas y los tag
ant_1 = 'PID=0403:6015 SER=D200C017A'
ant_2 = 'PID=0403:6015 SER=D200BZVHA'
tag_1 = ":CCF957966AC9"
tag_2 = ":CCF957966B2C"

#Solicitamos los datos importantes para almacenarlos en la base de datos
campo_vision = int(input('Linea de visión, ¿está libre de objetos? (no = 0 y si = 1):  '))
altura_ant = int(input('Ingresa la altura a la que se encuentra la antena en cm:  '))
dxy_en_cm = int(input('Ingresa la distancia entre la antena y el tag en cm:  '))
dz_en_cm = int(input('Ingresa la áltura a la que se encuentra el tag en cm:  '))
os.system('cls')

print('~'*50)       
U_Blox = serial.Serial(str(find_port(ant_2)),115200,timeout=2,write_timeout=1)
print(U_Blox)

for num in range(2):
    #Datos
    named_tuple = time.localtime()
    time_string = time.strftime("%Y%m%d_%H%M%S",named_tuple)
    archivo = time_string + '.csv'
    archivo = 'Base_datos//LOS_libre' + archivo

    adquisicion_datos(archivo,n,U_Blox,tag_2,campo_vision,altura_ant,dxy_en_cm,dz_en_cm)
    print("Número de iteraciones: ",num)

U_Blox.close()

