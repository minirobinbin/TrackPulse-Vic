from utils.search import *
from utils.checktype import *
import discord

import json

def checkRareTrainsOnRoute():

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
    
    rareFound = []
    
    # get data for all routes
    for route in RouteID:
        # read train type from data
        api_response = runs_api_request(route['route_id'])
        json_response = json.dumps(api_response)
        data = json.loads(json_response)

        # Extract relevant information from runs with vehicle data and check for target models
        print(f"Route ID: {route['route_id']}, Name: {route['route_name']}")
        for run in data['runs']:
            if run['vehicle_position']:
                vehicle_type = run['vehicle_descriptor']['description']
                try:
                    cars = run['vehicle_descriptor']['id'].split("-")
                except Exception as e:
                    print(f'Error: {e}')
                # print(f'cars DEBUG {cars}')
                
                vehicle_type = trainType(cars[0]) # get vhecle type from 1st number
                
                # print(f"Vhercle type: {vehicle_type}")
                train_model = vehicle_type # just cause im lazy to update
                if route['route_name'] == 'Mernda' or route['route_name'] == 'Belgrave' or route['route_name'] == 'Alamein' or route['route_name'] == 'Glen Waverley' or route['route_name'] == 'Hurstbridge':
                    rareTrains = ["Alstom Comeng", "EDI Comeng", "Comeng", "Siemens Nexas", "Siemens", "HCMT"]

                    if any(model in train_model for model in rareTrains):
                        # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')
                            
                elif route['route_name'] == 'Lilydale':
                    rareTrains = ["Alstom Comeng", "EDI Comeng", "Comeng", "Siemens Nexas", "Siemens", "HCMT"]

                    if any(model in train_model for model in rareTrains):
                        # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')

                        
                elif route['route_name'] == 'Craigieburn' or route['route_name'] == 'Upfield' or route['route_name'] == 'Upfield' or route['route_name'] == 'Sandringham':
                    rareTrains = ["X'Trapolis 100","Xtrapolis", "HCMT"]

                    if any(model in train_model for model in rareTrains):
                        # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')
                
                elif route['route_name'] == 'Frankston' or route['route_name'] == 'Werribee' or route['route_name'] == 'Williamstown':
                    rareTrains = ["HCMT"]

                    if any(model in train_model for model in rareTrains):
                        # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')
                            
                elif route['route_name'] == 'Pakenham' or route['route_name'] == 'Cranbourne':
                    rareTrains = ["X'Trapolis 100", "EDI Comeng","Alstom Comeng","Comeng", "Siemens Nexas", "Siemens"]

                    if any(model in train_model for model in rareTrains):
                        # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')
                        
                elif route['route_name'] == 'Sunbury':
                    rareTrains = ["X'Trapolis 100", "Xtrapolis"]

                    if any(model in train_model for model in rareTrains):
                       # THING TO CHECK IF PTV API IS SPREADING MISINFOMRATION ONLINE
                        print(f"Checking for misinformation in {run['vehicle_descriptor']['id']}")
                        cars = run['vehicle_descriptor']['id'].split("-")
                        misinformation_found = False
                        for car in cars:
                            carType = trainType(car)
                            if carType not in rareTrains:
                                print("Misinformation found!")
                                misinformation_found = True
                                break

                        if not misinformation_found:
                            print(f"Run ID: {run['run_id']}")
                            print(f"Train type: {vehicle_type}")
                            print(f"Train ID: {run['vehicle_descriptor']['id']}")
                            print("This run has a target train type.")
                            rareFound.append(f"{route['route_name']} - Train {vehicle_type}\nNumber {run['vehicle_descriptor']['id']}")
                            print()
                        else:
                            print('No rare trains found')
                
                else:
                    print('invalid route')
        print(rareFound)
    return(rareFound)


# checkRareTrainsOnRoute()