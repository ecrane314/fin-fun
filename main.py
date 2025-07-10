"""
Create a json file with tickers, here called tickers_config.json
[
  "key_alpha",
  "key_beta",
  "key_gamma",
  // ... up to 100 keys
  "key_omega"
]

After bootstrap done successfully,
Get ticker json list from gcs
Push list to ticker topic
Pull ticker, get data from APIs
Write payload to payload topic
"""

import os

import pubsub_messaging as pubsub
from polygon_get_option_contract_overview import get_REST_option_contract_overview


if __name__ == "__main__":
    # ticker = pull_from_subscription()

    topic = os.getenv("REQUESTS_TOPIC")
    payload = open("./tickers_config.json", "rb").read()
    
    print(topic)
    print(payload)

    pubsub.push_ticker_to_topic(topic, payload)
    

    # payload = os.getenv("PAYLOAD_TOPIC")
    # json_payload = get_REST_option_contract_overview()
    # pubsub.push_to_schema_topic(payload, json_payload)

    # acknowledge_message()