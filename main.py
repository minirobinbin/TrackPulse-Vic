from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *

# convertTrainLocationToGoogle(getTrainLocation('955M'))

train = '24M'
data = getTrainLocation(train)
for item in data:
    latitude = item['latitude']
    longitude = item['longitude']
    makeMap(latitude, longitude, train)