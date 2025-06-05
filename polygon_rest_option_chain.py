# import os
# api_key = os.environ.get('apiKey')


from polygon import RESTClient
from google.cloud import secretmanager

POLYGON_API_KEY = "projects/990799180178/secrets/polygon/versions/1"

ticker = "AAPL"

def key_from_secret_manager():
    '''retrieve key from GCP Secret Manager
    return type str'''
    with secretmanager.SecretManagerServiceClient() as client:
        response = client.access_secret_version(request={"name": POLYGON_API_KEY})
        key = response.payload.data.decode("UTF-8")
    return key


client = RESTClient(api_key=key_from_secret_manager())
def get_option_chain_from_polygon():
	contract = client.get_options_contract(
		"O:SPY251219C00650000"
		)
	print(contract)

if __name__ == "__main__":
	response = get_option_chain_from_polygon()
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