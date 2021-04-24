"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

neos_id = {}
neos = []
approaches = []

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    if not neo_csv_path:
        raise Exception('Cannot load data, no filename provided')

    filename = neo_csv_path
    with open(filename, 'r') as f:
        csv_file = csv.DictReader(f, delimiter=',')
        for row in csv_file:
            neo_data = {
                'name': row['name'],
                'pha': row['pha'],
                'diameter': row['diameter'],
                'pdes': row['pdes'],
            }
            neo = NearEarthObject(**neo_data)

            if neo.designation not in neos_id:
                neos_id[neo.designation] = len(neos)
                neos.append(neo)
    
    # TODO: Load NEO data from the given CSV file.
    return set(neos)
    

def load_approaches(cad_json_path):
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
    fields = contents['fields']

    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    key = {}
    for i in range(len(fields)):
        key[fields[i]] = i
    data = contents['data']
    count = 0
    for approach in data:
        approach_data = {
            "des": approach[key['des']],
            'cd': approach[key['cd']],
            'dist': approach[key['dist']],
            'v_rel': approach[key['v_rel']],
        }
        cad = CloseApproach(**approach_data)
        
        if cad._designation in neos_id:
            neo_index = neos_id[cad._designation]
            neo = neos[neo_index]
            cad.set_neo(neo)
            neo.add_cad(cad)
            neos[neo_index] = neo

        approaches.append(cad)            
    return list(set(approaches))
