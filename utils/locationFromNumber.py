from utils.search import *
import json

def getTrainLocation(Tnumber):
    data = runs_api_request(9)
    
    for entry in data:
        vehicle_id = entry["vehicle_descriptor"]["id"]
        if Tnumber in vehicle_id:
            return entry["vehicle_position"]
    return None