#!/usr/bin/env python

"""Convert JSON to JSONL so that it can be loaded into the warehouse"""

import json
from google.cloud import pubsub_v1

IN_FILE = 'requests.temp'
OUT_FILE = 'requsts.jsonl.temp'
JSON_SUB = 'fred-json-sub'
JSONL_TOPIC = 'fred-jsonl'
PROJECT = 'crane-gcp'


def load_json_file(in_file=IN_FILE):
    '''Open local json file for reading'''
    with open(in_file, 'r', encoding='utf-8') as file:
        # Load json for text or binary files, object will make dict
        # https://docs.python.org/3/library/json.html#json.load
        json_input = json.load(file)
        return json_input


def write_jsonl_file(json_input, out_file=OUT_FILE):
    '''Write entries from dict per line to achieve jsonl'''
    with open(out_file, 'w', encoding='utf-8') as out:
        # Pull value entries from observations key in dict
        for i in json_input['observations']:
            json_out = json.dumps(i) + '\n'
            out.write(json_out)
        out.close()


def pull_json_from_subscription(subscription = JSON_SUB, project = PROJECT):
    '''Load JSON data from a Google PubSub subscription'''
    sub_client = pubsub_v1.SubscriberClient()
    sub = sub_client.subscription_path(project, subscription)
    print (sub_client.pull(sub))
#TODO pull not set correctly. Continue reading here. 
https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.client.Client#google_cloud_pubsub_v1_subscriber_client_Client_pull

if __name__=="__main__":
    pull_json_from_subscription()
