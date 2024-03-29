#!/usr/bin/env python

"""Extract data series from FRED API
Feb 2023

UPDATE --- abandoning this module as PubSub is not the correct data plane for this bulk load
Using GCS instead. PubSub would be correct if each observation were a single message.
PubSub will be used for GCS finalization notifications, scheduling, and other orchestration
"""


# import requests
# from google.cloud import secretmanager
# from google.cloud import storage
# from google.cloud import pubsub_v1


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


secret_client = secretmanager.SecretManagerServiceClient()
def get_fred(series):
    '''Fetch a series from FRED API using key in GCP Secret Manager'''
    response = secret_client.access_secret_version(request={"name": FRED_API})
    key = response.payload.data.decode("UTF-8")

    # Observations to file
    response2 = requests.get(f'https://api.stlouisfed.org/fred/series/observations?\
        series_id={series}&api_key={key}&file_type=json', timeout=5)
    return response2.content


publisher = pubsub_v1.PublisherClient()
def publish_to_topic(data):
    '''Write bytestring data to PubSub topic'''
    topic_path = publisher.topic_path(project=PROJECT, topic=TOPIC)
    print("=====data=====")
    print(type(data))

    future = publisher.publish(topic_path, data)
    print("Result: " + future.result())


if __name__ == "__main__":
    series_list = get_series()
    print(series_list)

    for i in series_list:
        print("Series: " + i)
        publish_to_topic(get_fred(i))
