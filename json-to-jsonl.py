#!/usr/bin/env python

"""Convert JSON to JSONL so that it can be loaded into the warehouse"""

#from pandas.io.json import json_normalize
#import pandas as pd
import json

in_file = 'requests.temp'
out_file = 'requsts.jsonl.temp'

# Open json file for read
f = open(in_file, 'r')

# Load json for text or binary files, object will make dict
# https://docs.python.org/3/library/json.html#json.load
json_input = json.load(f)

#TODO BROKEN
# Write entries from dict per line to achieve jsonl
out = open(out_file, 'w')
for i in json_input:
    json_out = json.dumps(i) + '\n'
    out.write(json_out)
out.close()