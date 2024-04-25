import os
import csv
import pandas as pd
import seaborn as sns
import json
from utils.search import *
from matplotlib import pyplot as plt

def add_to_csv(data):
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['run_id', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for entry in data:
            if 'vehicle_position' in entry and entry['vehicle_position'] is not None:
                latitude = entry['vehicle_position']['latitude']
                longitude = entry['vehicle_position']['longitude']
                writer.writerow({'run_id': entry['run_id'], 'latitude': latitude, 'longitude': longitude})
                print(f"Added run_id: {entry['run_id']} with latitude: {latitude}, longitude: {longitude} to CSV")



def genMap():
    # File access
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "train_locations.csv")
    image_path = os.path.join(current_dir, "Potatoe.png")
    
    try:
        # Open CSV file in write mode with newline='' for Windows compatibility
        with open(data_path, 'w', newline='') as csv_file:
            header = ['Latitude', 'Longitude']
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            
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
    
            
            # Get data for all routes
            for route in RouteID:
                # Read train type from data
                api_response = runs_api_request(route['route_id'])  # Assuming this function works correctly
                json_response = json.dumps(api_response)
                data = json.loads(json_response)
                
                # Loop through 'runs' in the JSON data
                for run in data['runs']:
                    if run.get('vehicle_position'):
                        lat = run['vehicle_position'].get('latitude', '')
                        lon = run['vehicle_position'].get('longitude', '')
                        csv_writer.writerow([lat, lon])
                        print(f'Appended: lat {lat}, long {lon} to the csv')
    except Exception as e:
        print(f"An error occurred: {e}")

    # read the csv 
    df = pd.read_csv(data_path, skiprows=1, names=['Latitude', 'Longitude'])
    print(df.head())

    # thing to filter the data
    # state = 'VIC'
    # status = 'Operational'
    # filtered_df = df[df['state'] == state]
    # filtered_df = filtered_df[filtered_df['operationalstatus'] == status]


    # plot graph
    sns.scatterplot(data=df, x="Longitude", y="Latitude")
    bg_image = plt.imread(image_path)
    plt.imshow(bg_image, aspect='auto')

    # settings
    # plt.xlim(-37.89974170269387, -38.08037565853107)  
    # plt.ylim(145.12596528142748, 144.72817232260618) 
    plt.legend([], frameon=False)
    plt.axis('off')
    
    # Save the specific area of the plot as an image
    plt.savefig(os.path.join(current_dir, "gen.png"), bbox_inches='tight', pad_inches=0.0)
    os.remove('utils/map/train_locations.csv')
