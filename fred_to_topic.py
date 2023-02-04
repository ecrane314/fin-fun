#!/usr/bin/env python

"""Extract data series from FRED API
Feb 2023"""

import requests
from google.cloud import secretmanager
from google.cloud import storage
from google.cloud import pubsub_v1


FRED_API = "projects/175540505188/secrets/fred-api/versions/1"
BUCKET = "crane-gcp"
SERIES = "fred/series"
TOPIC = "fred-json"
PROJECT = 'crane-gcp'


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


    # Observations to file
    response2 = requests.get(f'https://api.stlouisfed.org/fred/series/observations?\
        series_id={series}&api_key={key}&file_type=json', timeout=5)
    return response2


publisher = pubsub_v1.PublisherClient()
def publish_to_topic(data):
    '''Write bytestring data to PubSub topic'''
    topic_path = publisher.topic_path(project=PROJECT, topic=TOPIC)
    future = publisher.publish(topic_path, data.content)
    print(future.result())

if __name__ == "__main__":
    series_list = get_series()
    print(series_list)

    for i in series_list:
        print(i)
        publish_to_topic(get_fred(i))
    #TODO confirm message published works