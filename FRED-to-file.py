#!/usr/bin/env python

import os
import requests


# Load local FRED API key, no whitespace
#TODO Switch this to KMS
f = open('FRED-api.key', 'r')
key = f.read()
series = "DGS2"


# Results file
out = open('requests.temp', 'a')


# Series info to stdout
r = requests.get(f'https://api.stlouisfed.org/fred/series?series_id={series}&api_key={key}&file_type=json')
print(r.text)


# Observations to file
r2 = requests.get((f'https://api.stlouisfed.org/fred/series/observations?series_id={series}&api_key={key}&file_type=json'))
out.write(r2.text)
out.close()
