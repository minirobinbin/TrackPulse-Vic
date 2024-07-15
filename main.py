from utils.search import *
from utils.pageScraper import *
from utils.trainlogger.stats import *
from utils.locationFromNumber import *

# convertTrainLocationToGoogle(getTrainLocation('955M'))

# train = '444M'
# data = getTrainLocation(train)
# print(data)
# for item in data:
#     latitude = item['latitude']
#     longitude = item['longitude']
# print(f'Lat: {latitude} Long: {longitude}')
# makeMapv2(latitude, longitude, train)

# runs_api_request(9)
# runs_ref_api_request()
print(getGeopath(988179))
