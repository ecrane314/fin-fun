#!/usr/bin/env python

"""Extract data series from FRED API
January 2023"""

import requests
from google.cloud import secretmanager


FRED_API = "projects/175540505188/secrets/fred-api/versions/1"
SERIES = "DGS2"


# GCP Secret Manager hosts api key
with secretmanager.SecretManagerServiceClient() as client:
    response = client.access_secret_version(request={"name": FRED_API})
    key = response.payload.data.decode("UTF-8")

# Local file api key
#with open('FRED-api.key', 'r', encoding='utf-8') as f:
#   key = f.read()


# Results file
def get_fred(SERIES=SERIES):
    with open('requests.temp', 'a', encoding='utf-8') as out:

        # Series info to stdout
        r = requests.get(f'https://api.stlouisfed.org/fred/series?series_id={SERIES}&\
            api_key={key}&file_type=json', timeout=5)
        print(r.text)

        # Observations to file
        r2 = requests.get(f'https://api.stlouisfed.org/fred/series/observations?\
            series_id={SERIES}&api_key={key}&file_type=json', timeout=5)
        out.write(r2.text)
        out.close()


if __name__ == "__main__":
    # TODO load series from file "series.txt"
    with open("series.txt").readlines() as f:
        for i in f:
            get_fred(i)
    # TODO consider this in the cloud functions context