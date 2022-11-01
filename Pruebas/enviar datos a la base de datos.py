import requests
auth_data = {
    'user': 'Poxan',
    'pwd': '1234'}
headers = {
        'Content-Type': 'application/x-www-form-urlencoded'}
resp = requests.post('http://192.168.0.100/db/prueba.php',auth_data)
print(resp)

