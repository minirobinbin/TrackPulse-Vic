from utils.checktype import trainType
from utils.search import *
import json
import folium
from folium import plugins
from io import BytesIO
from PIL import Image
import threading

from utils.trainImage import getIcon

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

def getTrainLocation(Tnumber):
    def find_vehicle_by_descriptor_id(data, search_string):
        results = []
        parts = search_string.split('-')
        
        for run in data.get("runs", []):
            if run.get("vehicle_descriptor") and all(part in run["vehicle_descriptor"]["id"] for part in parts):
                results.append(run["vehicle_position"])
        
        return results

    def process_route(route):
        json_data = runs_api_request(route["route_id"])
        results = find_vehicle_by_descriptor_id(json_data, Tnumber)
        if results:
            all_results.extend(results)
    
    all_results = []
    threads = []
    
    for route in routes:
        thread = threading.Thread(target=process_route, args=(route,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return all_results

def convertTrainLocationToGoogle(data):
    def generate_google_maps_link(latitude, longitude):
        base_url = "https://www.google.com/maps/search/?api=1&query="
        coordinates = f"{latitude},{longitude}"
        return base_url + coordinates
    
    for item in data:
        latitude = item['latitude']
        longitude = item['longitude']
        google_maps_link = generate_google_maps_link(latitude, longitude)
        return google_maps_link
    
def makeMap(point_latitude, point_longitude, name):
    def create_map_and_save():
        try:
            # Get icon URL based on train type
            icon_url = 'https://xm9g.xyz/discord-bot-assets/metro.png'
            print(f'ICON URL: {icon_url}')
            icon = folium.CustomIcon(
                icon_url,
                icon_size=(50, 50),
            )        

            # Create a map centered around the point of interest
            map = folium.Map(location=[point_latitude, point_longitude], zoom_start=15, control_scale=False,)
            
            # Add a marker for the point of interest with custom icon
            folium.Marker([point_latitude, point_longitude], icon=icon, popup=name,).add_to(map)
            
            # Convert the map to PNG image
            print('starting png conversion')
            img_data = map._to_png()
            print('png conversion done')
            
            # Save the image to a file (optional)
            with open(f'temp/{name}-map.png', 'wb') as f:
                f.write(img_data)
            
            # Convert image data to PIL Image
            image = Image.open(BytesIO(img_data))
            
            # Crop image to square
            width, height = image.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = (width + size) // 2
            bottom = (height + size) // 2
            image = image.crop((left, top, right, bottom))
            
            # Save the cropped image to a file (optional)
            image.save(f'temp/{name}-map.png')
                
        except Exception as e:
            print(f'Error creating map: {e}')

    thread = threading.Thread(target=create_map_and_save)
    thread.start()

