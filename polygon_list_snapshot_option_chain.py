"""
Pull a ticker from a pubsub subscription.
Get that option chain from polygon.
Print it and ack the message.
"""

import os
from polygon import RESTClient
from google.cloud import secretmanager
from google.cloud import pubsub_v1


def key_from_secret_manager():
    '''retrieve key from GCP Secret Manager
    return type str'''
    with secretmanager.SecretManagerServiceClient() as client:
        response_key = client.access_secret_version(request= "name": os.environ.get('POLYGON_API_KEY'))
        key = response_key.payload.data.decode("UTF-8")
    return key


#GEM should the client be outside of the function for reuse?
#TODO create pubsub client
pubsub_client = pubsub_v1.SubscriberClient()
def pull_from_subscription():
     #TODO get a ticker from pubsub
    result = pubsub_client.pull(REQUESTS_SUBSCRIPTION)
    return result


def acknowledge_message(subscription_id, message_id):
    #TODO acknowledge message after pulled
    pubsub_client.acknowledge(subscription_id, message_id)


polygon_client = RESTClient(api_key=key_from_secret_manager())
def get_option_chain_from_polygon(ticker, results_limit=10):
# https://polygon.io/docs/rest/options/snapshots/option-chain-snapshot
    options_chain = []
    for o in polygon_client.list_snapshot_options_chain(
        ticker,
        params={
            "order": "asc",
            "limit": results_limit,
            "sort": "ticker"
        }
	):
        options_chain.append(o)
    return options_chain



if __name__ == "__main__":
    try:
        target_ticker = pull_from_subscription()

        response = get_option_chain_from_polygon(target_ticker)
        if response.status == OK:
            acknowledge_message(response.messageID)

        print(response)

    except:
        print ("Could not pull from subscription")
