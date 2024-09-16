from utils.routeName import get_route_name
from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *
from ptv.client import PTVClient

########### Python 3.2 #############
import urllib.request, json

try:
    url = "https://data-exchange-api.vicroads.vic.gov.au/opendata/v1/gtfsr/metrotrain-tripupdates"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': '67397afc99c74afd9c6196ab4cfcce33',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)
####################################
