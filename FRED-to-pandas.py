#!/usr/bin/env python

import requests
from pandas.io.json import json_normalize
import pandas as pd

# https://pythonbasics.org/pandas-json/

url = "https://api.exchangerate-api.com/v4/latest/USD"
df = pd.read_json(url)

#TODO  IS THIS VALID JSON OUTPUT?
#TODO put the key for the FRED request in KMS, load library here

print(df)