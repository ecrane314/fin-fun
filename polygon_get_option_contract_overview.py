"""
Get that option chain from polygon.
Print it and ack the message.
"""

import os
import json
import requests
from polygon import RESTClient
from google.cloud import secretmanager


def key_from_secret_manager():
    '''retrieve key from GCP Secret Manager
    return type str'''
    with secretmanager.SecretManagerServiceClient() as client:
        response_key = client.access_secret_version(request={"name": \
                os.environ.get('POLYGON_API_KEY')})
        key = response_key.payload.data.decode("UTF-8")
    return key

api_key = key_from_secret_manager()


def get_REST_option_contract_overview():
    url ="https://api.polygon.io/v3/reference/options/contracts/O:SPY251219C00750000"
    url_suffix="?apiKey=" + api_key
    
    response = requests.get(url + url_suffix)
    print(response.json())


polygon_client = RESTClient(api_key)
def get_option_contract_overview():
    contract = polygon_client.get_options_contract(
        "O:SPY251219C00750000"
    )
    return contract


if __name__ == "__main__":
    # get_option_contract_overview()
    get_REST_option_contract_overview()