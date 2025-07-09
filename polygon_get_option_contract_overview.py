"""
Get that option chain from polygon.
Print it and ack the message.
"""

import os
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
    '''Use REST endpoint, get contract overview'''
    url ="https://api.polygon.io/v3/reference/options/contracts/O:SPY251219C00700000"
    url_suffix="?apiKey=" + api_key
    
    response = requests.get(url + url_suffix)
    response.raise_for_status()  #GCA It's good practice to check for request errors
    # type is class 'bytes' > response.content
    # type is class 'dict' > response.json()
    # print(json.dumps(response.json()))
    return response.content


polygon_REST_client = RESTClient(api_key)
def get_option_contract_overview():
    '''Use Python REST client library, get contract overview'''
    contract = polygon_REST_client.get_options_contract(
        "O:SPY251219C00750000"
    )
    return contract


if __name__ == "__main__":
    # get_option_contract_overview()
    # print(api_key)
    get_REST_option_contract_overview()