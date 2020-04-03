import requests

r = requests.get('https://covidtracking.com/api/states/daily')

with open('data.json', 'wb') as f:
    f.write(r.content)
