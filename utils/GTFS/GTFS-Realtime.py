from google.transit import gtfs_realtime_pb2
import requests
from dotenv import load_dotenv
import os

feed = gtfs_realtime_pb2.FeedMessage()
load_dotenv()
api_key = os.getenv('VIC_TRANSPORT_API_KEY')

headers = {'Ocp-Apim-Subscription-Key': api_key}
response = requests.get('https://data-exchange-api.vicroads.vic.gov.au/opendata/v1/gtfsr/metrotrain-tripupdates', headers=headers)
feed.ParseFromString(response.content)
for entity in feed.entity:
    if entity.HasField('trip_update'):
        print(entity.trip_update)