# from utils.routeName import get_route_name
# from utils.search import *
# from utils.pageScraper import *
# from utils.trainlogger.stats import *
# from utils.locationFromNumber import *
from utils.stoppingpattern import *
import asyncio

from utils.trainlogger.stationDistance import getStationDistance, load_station_data
from utils.trainlogger.stats import getLongestTrips
# # from ptv.client import PTVClient


print(getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), 'Ringwood','Flinders Street'))