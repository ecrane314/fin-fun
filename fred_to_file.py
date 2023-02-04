#!/usr/bin/env python

"""Extract data series from FRED API
January 2023"""

import requests
from google.cloud import secretmanager
from google.cloud import storage


FRED_API = "projects/175540505188/secrets/fred-api/versions/1"
BUCKET = "crane-gcp"
# Leading / on object name will return type none
SERIES = "fred/series"


# Local file api key
#with open('FRED-api.key', 'r', encoding='utf-8') as f:
#   key = f.read()


storage_client = storage.Client()

def get_series(bucket=BUCKET, series_file=SERIES):
    '''Fetch series file from GCS and write to list'''

    bucket_obj = storage_client.bucket(bucket)
    blob_obj = bucket_obj.get_blob(series_file)
    blob = blob_obj.download_as_text()

    return blob.split()


def get_fred(series):
    '''Fetch a series from FRED API using key in GCP Secret Manager'''
    with secretmanager.SecretManagerServiceClient() as client:
        response = client.access_secret_version(request={"name": FRED_API})
        key = response.payload.data.decode("UTF-8")


    with open('requests.temp', 'a', encoding='utf-8') as out:
        # Series info to stdout
        response = requests.get(f'https://api.stlouisfed.org/fred/series?series_id={series}&\
            api_key={key}&file_type=json', timeout=5)
        print(response.text)

        # Observations to file
        response2 = requests.get(f'https://api.stlouisfed.org/fred/series/observations?\
            series_id={series}&api_key={key}&file_type=json', timeout=5)
        out.write(response2.text)
        out.close()


if __name__ == "__main__":
    series_list = get_series()
    print(series_list)

    for i in series_list:
        print(i)
        #get_fred(i)
