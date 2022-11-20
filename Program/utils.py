import serial
import serial.tools.list_ports
import requests
import os
import time

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

def enviar_datos_php_test(hora,I_t,RSSI,A_a,A_e,canal,LOS,a_a,d_a,A_t):
    print("ingresaste a la funcion php")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'}
    
    auth_data = {
        'hora':hora,
        'Iden_tag':I_t,
        'RSSI':RSSI,
        'Ang_azimuth':A_a,
        'Ang_elevacion':A_e,
        'Canal':canal,
        'LOS':LOS,
        'Altura_ant':a_a,
        'Distancia_entre_ant_tag':d_a,
        'Altura_tag':A_t}

    resp = requests.post('http://192.168.0.100/crud/procesos/insertar.php',data=auth_data)
    print("dato enviado por php")
    resp

def adquisicion_datos_php_test(iteraciones,Antena,Puerto,tag,campo_vision,altura_ant,dxy_en_cm,dz_en_cm,variacion_mediciones):
    
    campos = ['Hora','Antena','Iden_tag','RSSI','Ang_azimuth','Ang_elevacion','RSSI_2','Canal','LOS(si=1,no=0)','Altura_ant(cm)','Distancia_entre_ant_tag(cm)','Altura_tag(cm)','Error_dato_medido']

    while(contador<iteraciones):
        os.system('cls')
        print("Guardando dato número: ",contador)

        # La hora
        time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

        # Recolectando los datos
        line = Puerto.readline().decode('utf-8')
        print(line)
        if tag in line:
            x = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p = int(x[1])
                Azimuth_angle = int(x[2])
                Elevation_angle = int(x[3])
                RSSI_2p = int(x[4])
                Adv_Channel = str(x[5])
                Adv_Channel = int(Adv_Channel)
                print("Dato recibido correctamente")
                    
                contador = contador + 1    
                enviar_datos_php(time_string,tag,RSSI_1p,Azimuth_angle,Elevation_angle,Adv_Channel,campo_vision,altura_ant,dxy_en_cm,dz_en_cm)
            except: 
                pass     
        else:
            print("Dato recibido de forma incorrecta")

def enviar_datos_php(hora,I_t,RSSI,A_a,A_e,canal,LOS,a_a,d_a,A_t,ant):
    print("ingresaste a la funcion php")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'}
    
    auth_data = {
        'hora':hora,
        'Iden_tag':I_t,
        'RSSI':RSSI,
        'Ang_azimuth':A_a,
        'Ang_elevacion':A_e,
        'Canal':canal,
        'LOS':LOS,
        'Altura_ant':a_a,
        'Distancia_entre_ant_tag':d_a,
        'Altura_tag':A_t,
        'Antena':ant}

    resp = requests.post('http://192.168.0.100/crud/procesos/insertar.php',data=auth_data)
    print("dato enviado por php")
    resp

def adquisicion_datos_php(iteraciones,Antena,Puerto,tag,campo_vision,altura_ant,dxy_en_cm,dz_en_cm):

    while(contador<iteraciones):
        # La hora
        time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

        # Recolectando los datos
        line = Puerto.readline().decode('utf-8')
        print(line)
        if tag in line:
            x = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p = int(x[1])
                Azimuth_angle = int(x[2])
                Elevation_angle = int(x[3])
                RSSI_2p = int(x[4])
                Adv_Channel = str(x[5])
                Adv_Channel = int(Adv_Channel)
                print("Dato recibido correctamente")
                    
                contador = contador + 1
                print("enviando dato")    
                enviar_datos_php(time_string,tag,RSSI_1p,Azimuth_angle,Elevation_angle,Adv_Channel,campo_vision,altura_ant,dxy_en_cm,dz_en_cm,Antena)
                print("dato enviado")
            except: 
                pass     
        else:
            print("Dato recibido de forma incorrecta")

def adquisicion_datos_test(iteraciones,Antena,Puerto,tag_1,tag_2):
    contador = 0
    tag_actual = ''

    while(contador<iteraciones):
        #os.system('cls')
        # La hora
        time_string = time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())

        # Recolectando los datos
        line = Puerto.readline().decode('utf-8')

        if tag_1 in line:
            x1 = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p_1 = int(x1[1])
                Azimuth_angle_1 = int(x1[2])
                Elevation_angle_1 = int(x1[3])
                RSSI_2p_1 = int(x1[4])
                Adv_Channel_1 = str(x1[5])
                Adv_Channel_1 = int(Adv_Channel_1)
                
                if(tag_actual!=tag_1):
                    print("Dato recibido correctamente")
                    print("RSSI:",RSSI_1p_1," ,A_a:",Azimuth_angle_1," ,A_e:",Elevation_angle_1," ,Canal",Adv_Channel_1, " ,Antena:",Antena," ,tag:",tag_1)
                    contador = contador + 1
            except: 
                pass  

        elif tag_2 in line:
            x2 = line.split(",")
            try: 
                #Identificador = str(x[0])
                RSSI_1p_2 = int(x2[1])
                Azimuth_angle_2 = int(x2[2])
                Elevation_angle_2 = int(x2[3])
                RSSI_2p_2 = int(x2[4])
                Adv_Channel_2 = str(x2[5])
                Adv_Channel_2 = int(Adv_Channel_2)
                
                if(tag_actual!=tag_2):
                    print("Dato recibido correctamente")
                    print("RSSI:",RSSI_1p_2," ,A_a:",Azimuth_angle_2," ,A_e:",Elevation_angle_2," ,Canal",Adv_Channel_2, " ,Antena:",Antena," ,tag:",tag_2)
                    contador = contador + 1
            except: 
                pass  
        
        else:
            print("Dato recibido de forma incorrecta")
        
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
        print("Estoy en el while")
        #os.system('cls')
        

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
                RSSI_2p_1 = int(x1[4])
                Adv_Channel_1 = str(x1[5])
                Adv_Channel_1 = int(Adv_Channel_1)
                
                if(tag_actual!=tag_1):
                    print("Dato recibido correctamente")
                    print("RSSI:",RSSI_1p_1," ,A_a:",Azimuth_angle_1," ,A_e:",Elevation_angle_1," ,Canal",Adv_Channel_1, " ,Antena:",Antena," ,tag:",tag_1)
                    enviar_php_datos_ant(time_string,tag_1,Antena,RSSI_1p_1,Azimuth_angle_1,Elevation_angle_1,Adv_Channel_1,Alt_ant)
                    time.sleep(0.1)
                    contador = contador + 1
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
                RSSI_2p_2 = int(x2[4])
                Adv_Channel_2 = str(x2[5])
                Adv_Channel_2 = int(Adv_Channel_2)
                
                if(tag_actual!=tag_2):
                    print("Dato recibido correctamente")
                    print("RSSI:",RSSI_1p_2," ,A_a:",Azimuth_angle_2," ,A_e:",Elevation_angle_2," ,Canal",Adv_Channel_2, " ,Antena:",Antena," ,tag:",tag_2)
                    enviar_php_datos_ant(time_string,tag_2,Antena,RSSI_1p_2,Azimuth_angle_2,Elevation_angle_2,Adv_Channel_2,Alt_ant)
                    time.sleep(0.1)
                    contador = contador + 1
            except: 
                pass  
        
        else:
            print("Dato recibido de forma incorrecta")
