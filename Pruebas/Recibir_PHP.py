import requests

resp = requests.get('http://192.168.0.100/crud/index.php')

data = resp.text

print(data)