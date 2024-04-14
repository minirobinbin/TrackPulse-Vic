import requests
import json
import queue


def montagueAPI(api_queue):
    # Define the URL
    url = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com/chumps.json"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data from the response
        data = response.json()
        
        # Get the first entry from the data
        first_entry = data[0]
        
        # Extract the required fields from the first entry
        date = first_entry["date"]
        thanks = first_entry["thanks"]
        streak = first_entry["streak"]
        chumps = first_entry["chumps"]
        image = first_entry["image"]
        thumb = first_entry["thumb"]
        date_year = first_entry["date_year"]
        date_week = first_entry["date_week"]
        date_aus_string = first_entry["date_aus_string"]
        
        # Create a dictionary with the extracted fields
        formatted_entry = {
            "date": date,
            "thanks": thanks,
            "streak": streak,
            "chumps": chumps,
            "image": image,
            "thumb": thumb,
            "date_year": date_year,
            "date_week": date_week,
            "date_aus_string": date_aus_string
        }
        
        # Print the formatted entry (optional)
        print(formatted_entry)
        api_queue.put(formatted_entry)
        
    else:
        print("Failed to fetch data from the URL.")
