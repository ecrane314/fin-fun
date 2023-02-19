#!/usr/bin/env python

"""Extract data series from FRED API
January 2023"""

import json
import requests
from google.cloud import secretmanager
from google.cloud import storage


FRED_API = "projects/175540505188/secrets/fred-api/versions/1"
BUCKET = "crane-gcp"
# Leading / on object name will return type none
SERIES = "fred/series"
OUTBOUND_GCS_PREFIX = "fred/outbound/"


def key_from_file():
    '''Local file api key
    No longer used, using secret manager'''
    with open('FRED-api.key', 'r', encoding='utf-8') as f01:
        key = f01.read()
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
    # response = requests.get(f'https://api.stlouisfed.org/fred/series?series_id={series}&\
    #     api_key={key}&file_type=json', timeout=5)
    # print(response.text)

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
    '''Loads input bytes as dict json object, add newlines between records,
    dumps() back to bytes  docs: 'Serialize obj to a JSON formatted str'
    return type is bytes'''

    # loads() input bytes as a json object, files instead use load()
    json_input = json.loads(input_bytes)
    jsonl_output = ""

    # Pull observations key in dict representation of json
    for i in json_input['observations']:
        jsonl_output += json.dumps(i) + '\n'

    # print(type(jsonl_output))
    return bytes(jsonl_output, 'utf-8')


def bytes_to_gcs(bucket_name, name, bytes_to_be_written):
    '''Write bytes to Google Cloud Storage object
    Input should be formatted in newline delimited JSONL so BigQuery can load'''

    bucket = storage_client.bucket(bucket_name)
    name = OUTBOUND_GCS_PREFIX + name
    blob = bucket.blob(name)

    with blob.open("wb") as f02:
        f02.write(bytes_to_be_written)


if __name__ == "__main__":
    series_list = get_series()

    for j in series_list:
        print(j)
        bytes_to_write = bytes_to_jsonl(get_fred(j, key_from_secret_manager()))
        bytes_to_gcs(BUCKET, j, bytes_to_write)
