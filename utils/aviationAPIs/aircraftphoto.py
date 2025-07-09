import requests

def getplaneimage(rego):
    url = f'https://api.planespotters.net/pub/photos/reg/{rego}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"