"""
Pull a ticker from a pubsub subscription.
Get that option chain from polygon.
Print it and ack the message.
"""

from polygon import RESTClient
from google.cloud import secretmanager
from google.cloud import pubsub


def key_from_secret_manager():
    '''retrieve key from GCP Secret Manager
    return type str'''
    with secretmanager.SecretManagerServiceClient() as client:
        response = client.access_secret_version(request={"name": POLYGON_API_KEY})
        key = response.payload.data.decode("UTF-8")
    return key


#GEM should the client be outside of the function for reuse?
#TODO create pubsub client
pubsub_client = pubsub.PubSubClient()
def pull_from_subscription():
     #TODO get a ticker from pubsub
     result = pubsub_client.pull(REQUESTS_SUBSCRIPTION)
     return result


def acknowledge_message(message_id):
     #TODO acknowledge message after pulled
     pubsub_client.ack(message_id)


polygon_client = RESTClient(api_key=key_from_secret_manager())
def get_option_chain_from_polygon(target_ticker):
    #TODO turn target ticker into format for polygon
    contract = polygon_client.get_options_contract(
    #TODO WHY is this getting a specific contract instead of a chain? 
		"O:SPY251219C00650000"
		)
	return contract


if __name__ == "__main__":
    #GEM Try catch   or  with as  construct?
    try( target_ticker = pull_from_subscription()):
        catch ("Could not pull from subscription")

    with response as get_option_chain_from_polygon(target_ticker):
	    if (response.status == OK):
            acknowledge_message(response.messageID)
    print(response)



""" contracts = []
for c in client.list_options_contracts(
	order="asc",
	limit=10,
	sort="ticker",
	):
    contracts.append(ticker)

print(contracts)
 """

""" 
# List Aggregates (Bars)
aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-01-01", to="2023-06-13", limit=50000):
    aggs.append(a)
print(aggs)

# Get Last Trade
trade = client.get_last_trade(ticker=ticker)
print(trade)

# List Trades
trades = client.list_trades(ticker=ticker, timestamp="2022-01-04")
for trade in trades:
    print(trade)

# Get Last Quote
quote = client.get_last_quote(ticker=ticker)
print(quote)

# List Quotes
quotes = client.list_quotes(ticker=ticker, timestamp="2022-01-04")
for quote in quotes:
    print(quote) """