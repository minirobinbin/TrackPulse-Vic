from utils.search import *

def getStationDisruptions(station):
    data = stationDisruption(station)
    disruptions = data.get('disruptions', {}).get('metro_train', [])
    
    disruption_list = []
    
    for disruption in disruptions:
        disruption_info = {
            "disruption_id": disruption['disruption_id'],
            "title": disruption['title'],
            "url": disruption['url'],
            "description": disruption['description'],
            "status": disruption['disruption_status'],
            "type": disruption['disruption_type'],
            "published_on": disruption['published_on'],
            "last_updated": disruption['last_updated'],
            "from_date": disruption['from_date'],
            "to_date": disruption['to_date'],
            "routes": [route['route_name'] for route in disruption['routes']],
            "stops": [stop['stop_name'] for stop in disruption['stops']]
        }
        disruption_list.append(disruption_info)
    
    return disruption_list
    