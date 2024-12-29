import os
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import json
from utils.search import runs_api_request

def add_to_csv(data):
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['run_id', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([
            {'run_id': entry['run_id'], 
             'latitude': entry['vehicle_position']['latitude'], 
             'longitude': entry['vehicle_position']['longitude']} 
            for entry in data if 'vehicle_position' in entry and entry['vehicle_position'] is not None
        ])

def generate_map():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "train_locations.csv")
    image_path = os.path.join(current_dir, "Potatoe.png")

    try:
        with open(data_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Latitude', 'Longitude'])

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
                {"route_id": 1482, "route_name": "Showgrounds - Flemington Racecourse"}
            ]

            all_locations = []
            for route in RouteID:
                api_response = runs_api_request(route['route_id'])  # Assuming this function returns a dictionary
                for run in api_response.get('runs', []):
                    if run.get('vehicle_position'):
                        lat = run['vehicle_position'].get('latitude', '')
                        lon = run['vehicle_position'].get('longitude', '')
                        all_locations.append([lat, lon])
                        print(f'Appended: lat {lat}, long {lon} to the csv')

            # Write all data at once for better performance
            csv_writer.writerows(all_locations)

    except Exception as e:
        print(f"An error occurred while processing routes: {e}")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_path, names=['Latitude', 'Longitude'])

    # Plot the data directly using pandas plot for simplicity
    fig, ax = plt.subplots(figsize=(10, 10))
    df.plot.scatter(x="Longitude", y="Latitude", ax=ax)
    ax.axis('off')
    
    # Save the plot as an image
    plt.savefig(os.path.join(current_dir, "gen.png"), bbox_inches='tight', pad_inches=0.0)

    # Clean up the CSV file
    os.remove(data_path)