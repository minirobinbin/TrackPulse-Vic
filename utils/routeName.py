from utils.search import routes_list
import json

def get_route_name(route_id):
    RouteID = [
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
    {"route_id": 1482, "route_name": "Showgrounds - Flemington Racecourse"},
    {"route_id": 99, "route_name": "City Loop"}
    ]
    
    for route in RouteID:
        if route["route_id"] == route_id:
            return route["route_name"]
        # else:
        #     vRoutes = routes_list(3)
        #     parsed_data = json.loads(vRoutes)

        #     def get_route_name(route_id):
        #         for route in parsed_data['routes']:
        #             if route['route_id'] == route_id:
        #                 return route['route_name']
        #         return None

            # route_name = get_route_name(1512)
            
    return f"Route name for ID {route_id} not found"

