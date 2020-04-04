import os
import csv
import copy
import json

DIR = os.path.dirname(__file__)
def rel(*p): return os.path.normpath(os.path.join(DIR, *p))

CENSUS_DATA = rel('nst-est2019-alldata.csv')
OUT_JSON = rel('state_data.json')

def main():
    state_data = copy.deepcopy(STATE_DATA)

    state_name_ind = {}     # { name: ind of record in STATE_DATA }
    state_abbrev_ind = {}   # { abbrev: ind of records in STATE_DATA }
    for i, v in enumerate(state_data):
        state_name_ind[v['name']] = i
        state_abbrev_ind[v['abbrev']] = i

    with open(CENSUS_DATA, 'r') as f:
        csv_r = csv.DictReader(f)
        for row in csv_r:
            name = row['NAME']
            population = int(row['POPESTIMATE2019'])

            if name not in state_name_ind:
                continue
            else:
                data_row_i = state_name_ind[name]
                state_data[data_row_i]['population'] = population

    state_json_data = {
        'name_ind': state_name_ind,
        'abbrev_ind': state_abbrev_ind,
        'data': state_data
    }

    state_json_str = json.dumps(state_json_data, indent=2)

    with open(OUT_JSON, 'w') as f:
        json.dump(state_json_data, f, indent=2)
	
STATE_DATA = [
    {"name": "Alabama", "abbrev": "AL"},
    {"name": "Alaska", "abbrev": "AK"},
    {"name": "Arizona", "abbrev": "AZ"},
    {"name": "Arkansas", "abbrev": "AR"},
    {"name": "California", "abbrev": "CA"},
    {"name": "Colorado", "abbrev": "CO"},
    {"name": "Connecticut", "abbrev": "CT"},
    {"name": "Delaware", "abbrev": "DE"},
    {"name": "Florida", "abbrev": "FL"},
    {"name": "Georgia", "abbrev": "GA"},
    {"name": "Hawaii", "abbrev": "HI"},
    {"name": "Idaho", "abbrev": "ID"},
    {"name": "Illinois", "abbrev": "IL"},
    {"name": "Indiana", "abbrev": "IN"},
    {"name": "Iowa", "abbrev": "IA"},
    {"name": "Kansas", "abbrev": "KS"},
    {"name": "Kentucky", "abbrev": "KY"},
    {"name": "Louisiana", "abbrev": "LA"},
    {"name": "Maine", "abbrev": "ME"},
    {"name": "Maryland", "abbrev": "MD"},
    {"name": "Massachusetts", "abbrev": "MA"},
    {"name": "Michigan", "abbrev": "MI"},
    {"name": "Minnesota", "abbrev": "MN"},
    {"name": "Mississippi", "abbrev": "MS"},
    {"name": "Missouri", "abbrev": "MO"},
    {"name": "Montana", "abbrev": "MT"},
    {"name": "Nebraska", "abbrev": "NE"},
    {"name": "Nevada", "abbrev": "NV"},
    {"name": "New Hampshire", "abbrev": "NH"},
    {"name": "New Jersey", "abbrev": "NJ"},
    {"name": "New Mexico", "abbrev": "NM"},
    {"name": "New York", "abbrev": "NY"},
    {"name": "North Carolina", "abbrev": "NC"},
    {"name": "North Dakota", "abbrev": "ND"},
    {"name": "Ohio", "abbrev": "OH"},
    {"name": "Oklahoma", "abbrev": "OK"},
    {"name": "Oregon", "abbrev": "OR"},
    {"name": "Pennsylvania", "abbrev": "PA"},
    {"name": "Rhode Island", "abbrev": "RI"},
    {"name": "South Carolina", "abbrev": "SC"},
    {"name": "South Dakota", "abbrev": "SD"},
    {"name": "Tennessee", "abbrev": "TN"},
    {"name": "Texas", "abbrev": "TX"},
    {"name": "Utah", "abbrev": "UT"},
    {"name": "Vermont", "abbrev": "VT"},
    {"name": "Virginia", "abbrev": "VA"},
    {"name": "Washington", "abbrev": "WA"},
    {"name": "West Virginia", "abbrev": "WV"},
    {"name": "Wisconsin", "abbrev": "WI"},
    {"name": "Wyoming", "abbrev": "WY"},
]

if __name__ == '__main__':
    main()


	
