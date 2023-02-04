#!/usr/bin/env python3

"""
Flask UI app
"""

#import requests
from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    """Base Hello World"""
    return "Hello, World!"

@app.route("/time")
def current_time():
    """Route to display current time"""
    return "The current time is " + str(datetime.now())

@app.route("/spx")
def get_spx():
    """Route to get current price for SP500"""
    #TODO Get key from environment variable. Pull from finnhub.io
    #    key = sys.
    return

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
