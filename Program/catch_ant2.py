from datetime import datetime
import time
import serial
import utils
import json

# Inicializando las variables
Altura_ant = 134        ## Esta debe estar en cm
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
U_Blox = serial.Serial(str(utils.find_port(ant_conexion)),115200) # en windows
print(U_Blox)

def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c
    return funcion_medida



try:
    while True:
        
        segundo_actual = datetime.today().second
        
        if segundo_actual == segundo_siguiente:
            print(str(time.strftime("%Y/%m/%d/ %H:%M:%S",time.localtime())))
            segundo_siguiente = segundo_siguiente + 1
            print("Entre al if exterior")
            if segundo_siguiente == 60 :
                segundo_siguiente = 0
            inicio = time.time()    
            utils.adquisicion_datos(4,ant_dato,U_Blox,tag_1,tag_2,Altura_ant)
            print(time.time()-inicio)
            print(segundo_actual)
            print(segundo_siguiente)
            
        
except KeyboardInterrupt:
    print("El usuario a detenido el programa")
    U_Blox.close()

except serial.SerialException:
    print("Error en la conexión con el programa")    
