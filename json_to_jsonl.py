#!/usr/bin/env python

"""Convert JSON to JSONL so that it can be loaded into the warehouse"""

import json
from google.cloud import pubsub_v1


IN_FILE = 'requests.temp'
OUT_FILE = 'requsts.jsonl.temp'
JSON_SUB = 'fred-json-sub'
JSONL_TOPIC = 'fred-jsonl'
MAX_MESSAGES = 1
#TODO Remove Project to config
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


def pull_json_from_subscription(project=PROJECT, sub=JSON_SUB):
    '''Load JSON data from a Google PubSub subscription'''
    #CLIENT, SUBSCRIPTION Constructor
    subscriber = pubsub_v1.SubscriberClient()
    source_sub = subscriber.subscription_path(project, sub)

    #DEFINE pull request
    request = pubsub_v1.types.PullRequest(subscription=source_sub,
        max_messages=MAX_MESSAGES)

    #PULL, response is <class 'google.cloud.pubsub_v1.types.PullResponse'>
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.types.PullResponse
    response = subscriber.pull(request=request)

    #EXIT if empty
    if len(response.received_messages) == 0:
        print("No messages: len(received_messages==0)")
        return

    # [Pull]response.received_messages is <class 'proto.marshal.collections.repeated.RepeatedComposite'>
    # MutableObject contains individual objects of type <class 'google.cloud.pubsub_v1.types.ReceivedMessage'>
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.types.ReceivedMessage
    # Contains an attribute 'message' class 'google.pubsub_v1.types.PubsubMessage' which...
    # contains an attribute 'data' which are the bytes
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.types.PubsubMessage
    ack_ids = []
    data_list =[]

    # i is 
    for i in response.received_messages:
        ack_ids.append(i.ack_id)
        data_list.append(i.message.data)
        i.ack()

    # ack_request = pubsub_v1.types.AcknowledgeRequest(subscription=source_sub, ack_ids=ack_ids)
    # subscriber.acknowledge(ack_request)

    return data_list



def publish_jsonl(json_input, project=PROJECT, topic=JSONL_TOPIC):
    '''Read JSON messages and publish JSONL to topic'''
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project=project, topic=topic)

    #json_input type <class 'list'>
    #TODO should return from pull_json_from_subscription() be a list?
        
    jsonl_out = []
   

    #TODO Confirm and fix the below, json_input is bytes
    for i in json_input:
        jsonl_out.append(json.dumps(i) + '\n')

    # publisher.publish(topic_path, jsonl_out)


if __name__=="__main__":
    # json_data is a list
    json_data = pull_json_from_subscription()
    publish_jsonl(json_data.pop())