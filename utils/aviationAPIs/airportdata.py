import requests

def get_airport_data(ICAO_code):
    url = f'https://airport-data.com/api/ap_info.json?icao={ICAO_code}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"