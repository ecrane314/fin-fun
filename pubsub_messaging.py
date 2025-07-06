"""
Pull a message from a pubsub subscription
Ack a pubsub message
Publish data to a pubsub topic with a schema
"""

import os
from google.cloud import pubsub_v1


sub_client = pubsub_v1.SubscriberClient()
pub_client = pubsub_v1.PublisherClient()


def pull_from_subscription():
    '''TODO get a ticker from pubsub'''
    result = sub_client.pull(REQUESTS_SUBSCRIPTION)
    return result


def acknowledge_message(subscription_id, message_id):
    #TODO acknowledge message after pulled
    sub_client.acknowledge(subscription_id, message_id)


def push_to_schema_topic(topic, payload):
    topic_path = pub_client.topic_path(os.environ.get("PROJECT_ID"), topic)
    pub_client.publish(topic_path, payload)
