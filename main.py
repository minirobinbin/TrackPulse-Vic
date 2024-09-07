from utils.routeName import get_route_name
from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *
from ptv.client import PTVClient


# ENV READING
env_path = '.env'
config = dotenv_values(env_path)


devId = config['DEV_ID']
key = config['KEY']

client = PTVClient(devId, key)


print(client.get_departures_from_stop(0, 1071))
