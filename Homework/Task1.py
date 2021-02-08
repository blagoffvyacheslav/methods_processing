import requests, json
response = requests.get('https://vk.cc/aARLzR')
data = response.json()
with open('response.json','w') as f:
    json.dump(data,f)