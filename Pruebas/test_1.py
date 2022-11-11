import requests
import json

r = requests.get('https://api.github.com/events')
r.json()

print(json.loads(r))