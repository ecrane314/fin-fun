#!/usr/bin/env python

"""Convert JSON to JSONL so that it can be loaded into the warehouse"""

#from pandas.io.json import json_normalize
#import pandas as pd
import json

filename = 'requests.temp'

# Open json file for read
f = open(filename, 'r')

# Load json for text or binary files, object will make dict
# https://docs.python.org/3/library/json.html#json.load
json_input = json.load(f)

#TODO Encode dict as jsonl?? Or is jsonl how I would dump it?

#TODO MAYBE needed json.dump() to file