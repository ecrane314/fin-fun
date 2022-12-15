#!/usr/bin/env python

import requests
from pandas.io.json import json_normalize
import pandas as pd

# https://pythonbasics.org/pandas-json/

url = "https://api.exchangerate-api.com/v4/latest/USD"
df = pd.read_json(url)

print(df)