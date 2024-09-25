import requests
from utils.keyCalc import *
import csv
import json

def search_api_request(search_term):
    # API endpoint URL
    url = getUrl(f"/v3/search/{search_term}")
    print(f"Search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

# Example usage
# search_term = 'Lilydale'
# search_api_request(search_term)

def route_api_request(route_id, route_type):
    
    # API endpoint URL
    url = getUrl(f'/v3/routes/?route_name={route_id}&route_types={route_type}')
    print(f"Route search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(formatted)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

def route_api_request_id(route_id):
    
    # API endpoint URL
    url = getUrl(f'/v3/routes/?route_id={route_id}')
    print(f"Route search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(formatted)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        
def routes_list(type):
    # API endpoint URL
    url = getUrl(f'/v3/routes/?route_types={type}')
    print(f"Route search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        formatted = format(data)
        print(formatted)
        formatted = json.dumps(data, indent=4)
        return(formatted)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

def runs_api_request(route_id):
    # API endpoint URL
    url = getUrl(f'/v3/runs/route/{route_id}?expand=All')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
def runs_ref_api_request(ref):
    # API endpoint URL
    url = getUrl(f'/v3/runs/{ref}?expand=All&include_geopath=true')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        # how to get run id for a specific set number?
        
def departures_api_request(stop_id, route_type):
    # API endpoint URL
    url = getUrl(f'/v3/departures/route_type/{route_type}/stop/{stop_id}?expand=All')
    print(f"search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        
        
def route_type_api_request():
    # API endpoint URL
    url = getUrl(f'/v3/route_types')
    print(f"search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        
def disruption_api_request(routeId):
    # API endpoint URL
    url = getUrl(f'/v3/disruptions/route/{routeId}')
    print(f"search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        
def specificRunAPIRequest(run_ref, route_type):
    # API endpoint URL
    url = getUrl(f'/v3/runs/{run_ref}/route_type/{route_type}?expand=VehiclePosition')
    print(f"search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

def fareEstimate(minZone:int, maxZone:int, touchOnUTC=None, touchOffUTC=None):
    # API endpoint URL
    urlString = f'/v3/fare_estimate/min_zone/{minZone}/max_zone/{maxZone}'
    if touchOnUTC != None:
        if '?' in urlString:
            marker ='&'
        else:
            marker = '?'
        touchOnUTC = touchOnUTC.replace(' ', '%20').replace(":", "%3A")
        urlString += f'{marker}journey_touch_on_utc={touchOnUTC}'

    if touchOffUTC != None:
        if '?' in urlString:
            marker ='&'
        else:
            marker = '?'
        touchOffUTC =touchOffUTC.replace(' ', '%20').replace(":", "%3A")
        urlString += f'{marker}journey_touch_off_utc={touchOffUTC}'


        
    url = getUrl(urlString)
    print(f"search url: {url}")
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the response data (assuming it's JSON)
        data = response.json()
        return(data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

def trainData(search_value):
    csv_filename = 'utils/metrotrains.csv'
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row[0] == search_value:
                return row
    return None

