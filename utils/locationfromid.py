from utils.search import *
import threading

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

def find_vehicle_by_descriptor_id(data, search_string):
    results = []
    
    for run in data.get("runs", []):
        if run.get("run_ref") == search_string:
            result = {
                "vehicle_position": run["vehicle_position"],
                "run_ref": run["run_ref"],
                "route_id": run["route_id"],
                "vehicle_descriptor": run["vehicle_descriptor"],
            }
            results.append(result)
    print(f'RESULTS THING: {results}')
    return results

def process_route(route, rid, all_results):
    json_data = runs_api_request(route["route_id"])  
    results = find_vehicle_by_descriptor_id(json_data, rid)
    if results:
        all_results.extend(results)

def getTrainLocationFromID(rid):
    all_results = []
    threads = []
    
    for route in routes:  
        thread = threading.Thread(target=process_route, args=(route, rid, all_results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return all_results