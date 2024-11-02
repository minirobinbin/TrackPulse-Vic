from utils.routeName import get_route_name
from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *
from utils.stoppingpattern import *

# from ptv.client import PTVClient

# print(getStoppingPattern(951228, 0))

########### Python 3.2 #############
import urllib.request, json

try:
    url = "https://data-exchange-api.vicroads.vic.gov.au/opendata/v1/gtfsr/metrotrain-servicealerts"

    hdr ={
    # Request headers
    'Ocp-Apim-Subscription-Key': '58e39e2654df47ee8c268ca56a059d95',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)
####################################
