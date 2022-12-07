import requests

# https://fred.stlouisfed.org/docs/api/fred/series.html is API Doc for Series
# Go to page of your series and snag the ID from the URL, DGS2# is 2 Year Treasuries, Daily
# Key is .gitignored in local file api.key, grab from your Fred account
# https://www.w3schools.com/python/ref_requests_get.asp 

https://api.stlouisfed.org/fred/series?series_id=GNPCA&api_key=<ADD API KEY FROM PASSWORDS>&file_type=json

two_year = requests.Request()

= GEt