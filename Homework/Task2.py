import requests, json
TOKEN = '***'
API_BASE =  'https://api.vk.com/method'
response = requests.get(
    f'{API_BASE}/groups.get',
    params={
        "access_token": TOKEN,
        "v": "5.110",
        "extended": 1,
    },
)
data = response.json()
with open('response_oauth.json','w') as f:
    json.dump(data,f)
