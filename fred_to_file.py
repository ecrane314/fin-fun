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

# Get series to pull
def get_series(bucket=BUCKET, series_file=SERIES):
    storage_client = storage.Client()
    #with storage.Client() as storage_client:
    bucket_obj = storage_client.bucket(bucket)
    blob_obj = bucket_obj.get_blob(series_file)
    blob = blob_obj.download_as_text()
    return blob.split()
    
    #print(type(blob))
    #print(blob)
    #print(type(blob_list))
    #print(blob_list)

# Results file
def get_fred(SERIES=list):
    # GCP Secret Manager hosts api key
    with secretmanager.SecretManagerServiceClient() as client:
        response = client.access_secret_version(request={"name": FRED_API})
        key = response.payload.data.decode("UTF-8")

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
    list = get_series()
    print(list)

    for i in list:
        print(i)
#TODO  Check get_fred writes to file as expected.
        #get_fred(i)
    # TODO consider this in the cloud functions context