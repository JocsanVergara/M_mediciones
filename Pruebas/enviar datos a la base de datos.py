import requests
#auth_data = {
#    'user': 'Poxan',
#    'pwd': '1234'}
headers = {
        'Content-Type': 'application/x-www-form-urlencoded'}
#resp = requests.post('http://192.168.0.100/db/prueba.php',auth_data)
#print(resp)

auth_data = {
    'hora':'2022/09/17/ 16:09:20',
    'Iden_tag':':CCF957966B2C',
    'RSSI':'-60',
    'Ang_azimuth':'-9',
    'Ang_elevacion':'-12',
    'Canal':'37',
    'LOS':'1.0',
    'Altura_ant':'134',
    'Distancia_entre_ant_tag':'30',
    'Altura_tag':'130'}

resp = requests.post('http://192.168.0.100/crud/procesos/insertar.php',data=auth_data)
resp
