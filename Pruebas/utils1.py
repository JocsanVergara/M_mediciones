import serial
import serial.tools.list_ports
import requests
import os
import time
import math


# Comando necesario para habilitar la lectura del puerto USB en ubuntu
# sudo chmod 666 /dev/ttyUSB0

def find_port(identf):
    """
        Esta función busca determinar el puerto serial que vamos a utilizar,
        se ingresa el identificador y si lo encuentra nos devuelve el nombre 
        del puerto al que esta conectado, de no ser así devuelve un 0. 
    """
    for port in serial.tools.list_ports.comports():
        if identf in str(port.hwid):
            return port.name

###-------------------------------------------------------------------------------------------------------------###

def enviar_php_datos_ant(hora,Id_tag,Id_ant,RSSI,A_a,A_e,canal,a_a):

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'}
    
    auth_data = {
        'hora':hora,
        'Id_tag':Id_tag,
        'Id_ant':Id_ant,
        'RSSI':RSSI,
        'Ang_azimuth':A_a,
        'Ang_elevacion':A_e,
        'Canal':canal,
        'Altura_ant':a_a,
        }
    resp = requests.post('http://192.168.0.100/crud/procesos/insertar.php',data=auth_data)
    resp

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
                    #print("Dato recibido correctamente")
                    #print("RSSI:",RSSI_1p_1," ,A_a:",Azimuth_angle_1," ,A_e:",Elevation_angle_1," ,Canal",Adv_Channel_1, " ,Antena:",Antena," ,tag:",tag_1)
                    enviar_php_datos_ant(time_string,tag_1,Antena,RSSI_1p_1,Azimuth_angle_1,Elevation_angle_1,Adv_Channel_1,Alt_ant)
                    time.sleep(0.1)
                    contador = contador + 1
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
                    #print("Dato recibido correctamente")
                    #print("RSSI:",RSSI_1p_2," ,A_a:",Azimuth_angle_2," ,A_e:",Elevation_angle_2," ,Canal",Adv_Channel_2, " ,Antena:",Antena," ,tag:",tag_2)
                    enviar_php_datos_ant(time_string,tag_2,Antena,RSSI_1p_2,Azimuth_angle_2,Elevation_angle_2,Adv_Channel_2,Alt_ant)
                    time.sleep(0.1)
                    contador = contador + 1
                    tag_actual = tag_2
            except: 
                pass  
        
        else:
            print("Dato recibido de forma incorrecta")

###-------------------------------------------------------------------------------------------------------------###

def CalculoAngulo(ang_11,ang_22):
    """
        Calculamos ambos ángulo formado entre las dos antenas y el tag
    """
    ang_1 = float(ang_11)
    ang_2 = float(ang_22)
    Alfa = 0.0
    Beta = 0.0
    if ang_1 > 0.0:
        #Caso 1: Ángulo 1 positivo y Ángulo 2 negativo
        if ang_2 < 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
        #Caso 2:
        elif ang_2 > 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
        #Caso 3:    
        elif ang_2 == 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0
            return Alfa,Beta 
    #caso 4:
    elif ang_1 < 0.0:
        if ang_2 < 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
    #Caso 5:
    elif ang_1 == 0.0:
        if ang_2 < 0.0:
            Alfa = 90.0
            Beta = 90.0 + ang_2
            return Alfa,Beta

def Distancia_ant_tag(d_entre_ants,Alfa,Beta):
    """
    Distancia entre el tag y la antena
    - Distancia entre ambas antenas
    - Alfa corresponde al ángulo de la antena 1 
    - Beta corresponde al ángulo de la antena 2
    a la salida tendremos dos distancias 
    """

    alfa, beta = CalculoAngulo(Alfa,Beta)

    # Distancia desde el punto C a A
    # con a definido como la distancia entre las dos antenas
    sigma = math.radians(180-beta-alfa)
    if(sigma!=0):
        B = d_entre_ants * math.sin(math.radians(alfa))/math.sin(sigma)  # b=a*sin(beta)/sin(sigma)
        A = d_entre_ants * math.sin(math.radians(beta))/math.sin(sigma) # c=a*sin(alfa)/sin(sigma)
    else:
        A = 0
        B = 0
    # la altura del triangulo que se forma entre las dos distancias B y C
    #h = d_entre_ants * (math.sin(math.radians(alfa))*math.sin(math.radians(beta))) / math.sin(math.radians(alfa+beta))
    return B,A

###-------------------------------------------------------------------------------------------------------------###