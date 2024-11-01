from utils.search import *
import json

def getStoppingPattern(routeId, routeType):
    json_data = stoppingPatternAPIRequest(routeId, routeType)

    stops = json_data['stops']
    stops_list = []
    
    # Iterate through each stop in the stopping pattern
    for stop_id, stop_info in stops.items():
        stop_data = {
            "stop_id": stop_id,
            "stop_name": stop_info["stop_name"],
            "suburb": stop_info["stop_suburb"],
            "zone": stop_info["stop_ticket"]["zone"],
            "latitude": stop_info["stop_latitude"],
            "longitude": stop_info["stop_longitude"]
        }
        stops_list.append(stop_data)

    return stops_list