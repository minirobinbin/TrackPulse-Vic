from utils.routeName import get_route_name
from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *
from utils.stoppingpattern import *
from utils.trainlogger.logembed import *

# from ptv.client import PTVClient

# print(getStoppingPattern(951228, 0))


import requests

# URL of the API endpoint
url = "https://data-exchange-api.vicroads.vic.gov.au/opendata/v1/gtfsr/metrotrain-tripupdates"

# Headers for the request
headers = {
    "Cache-Control": "no-cache",
    "Ocp-Apim-Subscription-Key": "713db7df09e24badada81c928f745747"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # If successful, print the content of the response
    print(response.text)
else:
    # If not successful, print the status code and reason for the error
    print(f"Request failed with status code {response.status_code}: {response.reason}")