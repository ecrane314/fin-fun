"""
Pull a message from a pubsub subscription
Ack a pubsub message
Publish data to a pubsub topic with a schema
"""

import os
from google.cloud import pubsub_v1


sub_client = pubsub_v1.SubscriberClient()
pub_client = pubsub_v1.PublisherClient()

#messages to be sent
ticker_futures = []

def push_ticker_to_topic(topic, payload):
    topic = pub_client.topic_path(os.environ.get("PROJECT_ID"), topic)
    
    for i in payload:
        print(type(i))
        future = pub_client.publish(topic, bytes(i, 'utf-8'))
        ticker_futures.append(future)

    for j in ticker_futures:
       print(j.result())
    return

def pull_from_subscription():
    '''TODO get a ticker from pubsub'''
    result = sub_client.pull(os.environ.get("REQUESTS_SUBSCRIPTION"))
    return result


def acknowledge_message(subscription_id, message_id):
    #TODO acknowledge message after pulled
    sub_client.acknowledge(subscription_id, message_id)


def push_to_schema_topic(topic, payload):
    topic_path = pub_client.topic_path(os.environ.get("PROJECT_ID"), topic)
    
    # print(type(topic_path))
    # print(topic_path)
    
    # print(type(payload))
    # print(payload)
    
    future = pub_client.publish(topic_path, payload)
    print(future.result())
    futures.append(future)

if __name__ == "__main__":
    result = pull_from_subscription()

    acknowledge_message(result.id)