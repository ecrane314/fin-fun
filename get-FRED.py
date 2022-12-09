#!/usr/bin/env python

import os
import requests

# https://fred.stlouisfed.org/docs/api/fred/#API see fred/series and fred/series/observations
# Go to page of your series and snag the ID from the URL, DGS2 is 2 Year Treasuries, Daily
# Key is .gitignored in local file api.key, grab from your Fred account


# Pull in local API key from FRED account, no whitespace
f = open('FRED-api.key', 'r')
key = f.read()

out = open('requests.temp', 'a')

r = requests.get(f'https://api.stlouisfed.org/fred/series?series_id=DGS2&api_key={key}&file_type=json')
out.write(r.text)

r2 = requests.get((f'https://api.stlouisfed.org/fred/series/observations?series_id=DGS2&api_key={key}&file_type=json'))
out.write(r2.text)

out.close()
