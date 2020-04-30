import json
import requests

r = requests.get('https://covidtracking.com/api/v1/states/daily.json')
json_obj = json.loads(r.content)

with open('data.json', 'w') as f:
    json.dump(json_obj, f, indent=1)
