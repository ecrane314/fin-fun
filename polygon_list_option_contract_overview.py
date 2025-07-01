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
        response_key = client.access_secret_version(request={"name": \
                os.environ.get('POLYGON_API_KEY')})
        key = response_key.payload.data.decode("UTF-8")
    return key


#GEM should the client be outside of the function for reuse?
#TODO create pubsub client
pubsub_client = pubsub_v1.SubscriberClient()
def pull_from_subscription():
    '''TODO get a ticker from pubsub'''
    result = pubsub_client.pull(REQUESTS_SUBSCRIPTION)
    return result


def acknowledge_message(subscription_id, message_id):
    #TODO acknowledge message after pulled
    pubsub_client.acknowledge(subscription_id, message_id)


polygon_client = RESTClient(api_key=key_from_secret_manager())
def get_option_contract_overview():
    contract = polygon_client.get_options_contract(
        "O:SPY251219C00650000"
        )
    print(contract)



if __name__ == "__main__":
    get_option_contract_overview()
