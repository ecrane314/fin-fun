#!/usr/bin/env python

"""Convert JSON to JSONL so that it can be loaded into the warehouse"""

#from pandas.io.json import json_normalize
#import pandas as pd
import json

IN_FILE = 'requests.temp'
OUT_FILE = 'requsts.jsonl.temp'

# Open json file for read
with open(IN_FILE, 'r', encoding='utf-8') as f:

    # Load json for text or binary files, object will make dict
    # https://docs.python.org/3/library/json.html#json.load
    json_input = json.load(f)


# Write entries from dict per line to achieve jsonl
with open(OUT_FILE, 'w', encoding='utf-8') as out:

    # Pull value entries from observations key in dict
    for i in json_input['observations']:
        json_out = json.dumps(i) + '\n'
        out.write(json_out)
    out.close()
