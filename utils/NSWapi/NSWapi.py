import os
import requests
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

class NSWTransportAPI:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv('NSW_API_KEY')
        self.base_url = 'https://api.transport.nsw.gov.au/v2'

    def get_sydney_trains_positions(self):
        """Get real-time vehicle positions for Sydney Trains"""
        endpoint = f"{self.base_url}/gtfs/vehiclepos/sydneytrains"
        headers = {
            'Authorization': f'apikey {self.api_key}',
            'Accept': 'application/x-google-protobuf'
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            # Parse the protobuf response
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            return feed
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching vehicle positions: {e}")
            return None

print(NSWTransportAPI().get_sydney_trains_positions())