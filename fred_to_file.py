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



def key_from_file():
    '''Local file api key
    No longer used, using secret manager'''
    with open('FRED-api.key', 'r', encoding='utf-8') as f:
        key = f.read()
    return key



def key_from_secret_manager():
    '''retrieve key from GCP Secret Manager
    return type str'''
    with secretmanager.SecretManagerServiceClient() as client:
        response = client.access_secret_version(request={"name": FRED_API})
        key = response.payload.data.decode("UTF-8")
    return key



storage_client = storage.Client()
def get_series(bucket=BUCKET, series_file=SERIES):
    '''Fetch series file from GCS and write to list
    return type <class list>
    '''
    bucket_obj = storage_client.bucket(bucket)
    blob_obj = bucket_obj.get_blob(series_file)
    blob = blob_obj.download_as_text()

    return blob.split()


def get_fred(series, key):
    '''Fetch a series from FRED API using key in GCP Secret Manager
    return type is bytes, response also has text method to get unicode string
    '''
    # Series info to stdout
    response = requests.get(f'https://api.stlouisfed.org/fred/series?series_id={series}&\
        api_key={key}&file_type=json', timeout=5)
    print(response.text)

    # Observations to file
    response2 = requests.get(f'https://api.stlouisfed.org/fred/series/observations?\
        series_id={series}&api_key={key}&file_type=json', timeout=5)
    return response2.content


def bytes_to_file(response_bytes):
    '''Write input bytes to a local file.'''
    with open('requests.temp', 'a', encoding='utf-8') as out:
        out.write(response_bytes)
        out.close()


def bytes_to_jsonl(input_bytes):
    '''Encode input bytes as UTF-8, add newlines between records, dump back to bytes
    return type is bytes'''
    #TODO

def jsonl_to_gcs(bucket, name, bytes):
    '''Write bytes to Google Cloud Storage object
    Input should be formatted in newline delimited JSONL so BigQuery can load'''
    #TODO



if __name__ == "__main__":
    series_list = get_series()
    print(series_list)

    for i in series_list:
        print(i)
        #get_fred(i)
