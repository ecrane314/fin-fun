
#TODO research, every file is importing os to get env variables. Inefficient?
import os

from pubsub_messaging import pull_from_subscription, acknowledge_message, push_to_schema_topic
from polygon_get_option_contract_overview import get_REST_option_contract_overview



if __name__ == "__main__":
    # ticker = pull_from_subscription()

    PAYLOAD_TOPIC = os.getenv("PAYLOAD_TOPIC")

    json_payload = get_REST_option_contract_overview()
    push_to_schema_topic(PAYLOAD_TOPIC, json_payload)

    # acknowledge_message()