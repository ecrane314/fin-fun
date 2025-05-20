import os
api_key = os.environ.get('apiKey')


from polygon import WebSocketClient  # Imports the WebSocketClient class from the polygon library.
from polygon.websocket.models import WebSocketMessage, Feed, Market  # Imports specific data models related to WebSocket messages, feed types, and market types.
from typing import List  # Imports the List type hint for specifying lists.

client = WebSocketClient(  # Creates an instance of the WebSocketClient.
	api_key=api_key,  # Specifies your Polygon.io API key for authentication. **Important: Replace "YOUR_API_KEY" with your actual API key.**
	feed=Feed.Delayed,  # Sets the data feed to "Delayed", meaning you'll receive slightly delayed data.
	market=Market.Options  # Specifies that you are interested in options market data.
	)

# aggregates (per minute)
client.subscribe("AM.spy")  # Subscribes to aggregate (per minute) data for the "SPY" ticker in the options market (due to the 'Market.Options' setting). The "AM" prefix likely indicates aggregate minute data.

def handle_msg(msgs: List[WebSocketMessage]):  # Defines a function named "handle_msg" that takes a list of WebSocketMessage objects as input.
    for m in msgs:  # Iterates through each WebSocketMessage object in the input list "msgs".
        print(m)  # Prints the content of each received WebSocketMessage to the console.

# print messages
client.run(handle_msg)  # Starts the WebSocket client and registers the "handle_msg" function to be called whenever new messages are received. This will continuously print incoming data.