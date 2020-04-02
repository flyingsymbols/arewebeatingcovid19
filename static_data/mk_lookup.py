import csv
import json

CENSUS_DATA = 'nst-est2019-alldata.csv'

state_pops = {}
with open(CENSUS_DATA, 'r') as f:
	csv_r = csv.DictReader(f)
	for row in csv_r:
		state_pops[row['NAME']] = int(row['POPESTIMATE2019'])

state_pops_json = json.dumps(state_pops, indent=2)
print(state_pops_json)

with open('state_pops.json', 'w') as f:
	f.write(state_pops_json)
	
	
