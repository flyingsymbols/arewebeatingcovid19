import pandas
import json

with open('data.json', 'r') as f:
    df = pandas.read_json(f, orient='records')


