from utils.search import *
from utils.locationFromNumber import *
import json
import pytz
from datetime import datetime

routes = [
    {"route_id": 1, "route_name": "Alamein"},
    {"route_id": 2, "route_name": "Belgrave"},
    {"route_id": 3, "route_name": "Craigieburn"},
    {"route_id": 4, "route_name": "Cranbourne"},
    {"route_id": 5, "route_name": "Mernda"},
    {"route_id": 6, "route_name": "Frankston"},
    {"route_id": 7, "route_name": "Glen Waverley"},
    {"route_id": 8, "route_name": "Hurstbridge"},
    {"route_id": 9, "route_name": "Lilydale"},
    {"route_id": 11, "route_name": "Pakenham"},
    {"route_id": 12, "route_name": "Sandringham"},
    {"route_id": 13, "route_name": "Stony Point"},
    {"route_id": 14, "route_name": "Sunbury"},
    {"route_id": 15, "route_name": "Upfield"},
    {"route_id": 16, "route_name": "Werribee"},
    {"route_id": 17, "route_name": "Williamstown"},
    {"route_id": 1482, "route_name": "Showgrounds - Flemington Racecourse"}
]

def getStoppingPattern(runRef, routeType):
    if runRef is None:
        return None
    data = stoppingPatternAPIRequest(runRef, routeType)

    departures = data.get('departures', [])
    stops = data.get('stops', {})

    departures_info = []
    for departure in departures:
        stop_id = departure['stop_id']
        stop_info = stops.get(str(stop_id), {})
        stop_name = stop_info.get('stop_name', 'Unknown')
        scheduled_departure = departure.get('scheduled_departure_utc', 'Unknown')
        estimated_departure = departure.get('estimated_departure_utc', 'Unknown')

        # Add the current stop first
        departures_info.append((departure['departure_sequence'], stop_name, 
                                estimated_departure if estimated_departure else scheduled_departure, 'Scheduled'))

        # Then check for and add skipped stops
        skipped_stops = departure.get('skipped_stops', [])
        for skipped in skipped_stops:
            skipped_name = skipped.get('stop_name', 'Unknown')
            # remove "Station" from the name
            if skipped_name.endswith(' Station'):
                skipped_name = skipped_name[:-8]  # Remove " Station"
            # Use the same sequence number but add a small increment to ensure they come after the main stop
            departures_info.append((departure['departure_sequence'] + 0.1, skipped_name, 'Skipped', 'Skipped'))

    # Sort by departure_sequence
    sorted_departures = sorted(departures_info, key=lambda x: x[0])

    return [(name, time, status) for _, name, time, status in sorted_departures]

def getStoppingPatternFromCar(relistsData):
    runRef = None
    dataList = []

    for item in relistsData:
        runRef = item['run_ref']
        data = getStoppingPattern(runRef, 0)
        # print(f'F DATA: {data}')
        dataList.append(data)
        
    # Current time in Melbourne (AEST/AEDT)
    local_tz = pytz.timezone('Australia/Melbourne')
    current_time = datetime.now(local_tz)
    
    closest = None
    min_diff = float('inf')
    
    for data in dataList:
        if data:  # Check if data is not empty
            first_time_str = data[0][1]
            utc_time = datetime.strptime(first_time_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
            local_time = utc_time.astimezone(local_tz)
            
            # Only consider times in the past or now
            if local_time <= current_time:
                time_diff = (current_time - local_time).total_seconds()
                if time_diff < min_diff:
                    min_diff = time_diff
                    closest = data

    return closest
                
def getStoppingPatternFromRunRef(relistsData, routeType):
    runRef = None
    dataList = []

    for item in relistsData:
        runRef = item['run_ref']
        data = getStoppingPattern(runRef, routeType)
        # print(f'F DATA: {data}')
        dataList.append(data)
        
    # Current time in Melbourne (AEST/AEDT)
    local_tz = pytz.timezone('Australia/Melbourne')
    current_time = datetime.now(local_tz)
    
    closest = None
    min_diff = float('inf')  # Initialize with infinity
    
    for data in dataList:
        if data:  # Check if data is not empty
            closest = data

    return closest
                