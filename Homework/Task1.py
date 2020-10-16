import requests, json
response = requests.get('https://api.github.com/users/blagoffvyacheslav/repos?sort=updated&direction=desc&visibility=all')
data = response.json()
with open('response.json','w') as f:
    json.dump(data,f)