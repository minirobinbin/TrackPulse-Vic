"this will be run every so oftern like 10 minutes to see when the train is"

import os
from commands.searchtrain import addmap
from utils.checktype import trainType
from utils.locationFromNumber import convertTrainLocationToGoogle, getTrainLocation, makeMapv2
from utils.routeName import get_route_name
from utils.stoppingpattern import getStoppingPatternFromCar
from utils.trainset import setNumber

async def getinfo(train):
    try:
        type = trainType(train)
        set = setNumber(train.upper())
        # Generate the map asynchronously
        # After map generation, send it
        if type == "HCMT": # because ptv api lists hcmts like "9005M-9905M" for some fucking reason
            hcmtcar1 = set.split('-')
            location = getTrainLocation(hcmtcar1[0]+'M')
        else:
            location = getTrainLocation(set)
        line = ""
        print(f"Location: {location}")
        url = convertTrainLocationToGoogle(location)
        try:
            stoppingPattern = getStoppingPatternFromCar(location)
        except Exception as e:
            return f'An error has occurred while searching for this trains run.'
        print(f"STOPPING PATTERN: {stoppingPattern}")
        
        # get final stop
        if stoppingPattern is None:
            stoppingPattern = "No stopping pattern found"
            lastStop = None
        else:
            lastStop = list(reversed(stoppingPattern))[0][0]

        try:
            if location is not None:
                for item in location:
                    latitude = item['vehicle_position']['latitude']
                    longitude = item['vehicle_position']['longitude']
                    line = get_route_name(item['route_id'])

                await makeMapv2(latitude,longitude, train, '') 
        except Exception as e:
            return(f'No trip data available\n{e}')

        file_path = f"temp/{train}-map.png"
        if os.path.exists(file_path):
                file = f"{train}-map.png"
                
                return file, line, url, stoppingPattern, train, lastStop
        else:
            return(f"Error: Map file '{file_path}' not found.")
    except Exception as e:
        return(f'There was an error generating the map:\n```{e}```')

async def seeWhereTrainsAre(trains:list):
    for train in trains:
        print(f"Checking where {train} is")
        return await getinfo(train)
        