import requests

def get_airport_data(ICAO_code):
    url = f'https://airport-data.com/api/ap_info.json?icao={ICAO_code}'
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"
    except requests.Timeout:
        return "Error: Request timed out"
