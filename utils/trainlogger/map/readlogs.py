from matplotlib.pylab import f
from utils.trainlogger.map.mapimage import MapImageHandler
from utils.trainlogger.map.station_coordinates_log_train_map_pre_munnel import x_offset as x_offset_log_train_map_pre_munnel, y_offset as y_offset_log_train_map_pre_munnel, station_coordinates as station_coordinates_log_train_map_pre_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import line_coordinates as lines_coordinates_log_train_map_pre_munnel

metro_date = '2025-12-31' # this is just a placeholder date, replace when the metro tunnel date is confirmed

def postprecompat(data:list, lines_dictionary:dict):
    newdata = []
    for line in data:
        cols = line.strip().split(',')
        if len(cols) >= 6:
            trip_date = cols[3]
            group = cols[4]
            station1=cols[5]
            station2=cols[6]
            trip_year = int(trip_date.split('-')[0])
            trip_month = int(trip_date.split('-')[1])
            trip_day = int(trip_date.split('-')[2])
            metro_year = int(metro_date.split('-')[0])
            metro_month = int(metro_date.split('-')[1])
            metro_day = int(metro_date.split('-')[2])
            if trip_year >= metro_year + 1 or (trip_year == metro_year and trip_month >= metro_month + 1) or (trip_year == metro_year and trip_month == metro_month and trip_day >= metro_day):
                if group == 'Frankston':
                    if station1 in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central'] and station2 in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = 'Unknown'
                    elif station1 in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station1 = '*Flinders Street'
                    elif station2 in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station2 = '*Richmond'
                elif group == 'Sandringham':
                    if station1 in lines_dictionary['Werribee'][0] and station2 in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif station1 in lines_dictionary['Williamstown'][0] and station2 in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},*South Yarra,')
                        station1 = '*Flinders Street'
                    elif station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},*South Yarra,')
                        station1 = '*Flinders Street'
                    elif station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,*South Yarra,{station2},')
                        station2 = '*Flinders Street'
                    elif station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,*South Yarra,{station2},')
                        station2 = '*Flinders Street'
                elif group == 'Werribee':
                    if station1 in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Sandringham'][0]:
                        group = 'Sandringham'
                    elif station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                        station2 = '*South Yarra'
                elif group == 'Williamstown':
                    if station1 in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Sandringham'][0]:
                        group = 'Sandringham'
                    elif station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                        station2 = '*South Yarra'
            line = f"{cols[0]},{cols[1]},{cols[2]},{trip_date},{group},{station1},{station2},"
        newdata.append(line)
    return newdata



def logMap(user:str, lines_dictionary:dict, mode:str='time_based_variants/log_train_map_pre_munnel.png', year:int=0):
    if mode == 'time_based_variants/log_train_map_pre_munnel.png':
        file = open(f'utils/trainlogger/userdata/{user}.csv', 'r')
        data = file.readlines()
        file.close()

        data = postprecompat(data, lines_dictionary)

        stations = []
        for line in data:
            cols = line.strip().split(',')
            
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                print(f"Trip year: {trip_year}")
                print(f"Year: {year}")
            
            # Only process if year is 0 (all years) or matches the specified year
            if year == 0 or trip_year == year:
                station1, station2 = cols[5], cols[6]
                if station1 not in stations:
                    stations.append(station1)
                if station2 not in stations:
                    stations.append(station2)
                    
        # split trips into individual segments
        expanded_data = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                
                # Only process if year is 0 (all years) or matches the specified year
                if year == 0 or trip_year == year:
                    start, end, group = cols[5], cols[6], cols[4]
                    start = start.replace('*','')
                    end = end.replace('*','')

                    # Find the line that contains these stations
                    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Glen Waverley', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sunbury', 'Upfield'] and cols[5] in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'City Circle' and start in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'Frankston' and start in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Frankston' and end in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Frankston' and start in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Frankston' and end in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Bendigo' and 'Epsom' in [str(start), str(end)]:
                        group = 'Epsom'
                    elif group == 'Bendigo' and 'Eaglehawk' in [str(start), str(end)]:
                        group = 'Eaglehawk'
                    if group == 'Werribee' and start not in ['Seaholme', 'Altona', 'Westona'] and end not in ['Seaholme', 'Altona', 'Westona']:
                        group = 'Werribee Express'
                    print(group)
                    for line_name, line_info in lines_dictionary.items():
                        if line_name == group:
                            station_list = line_info[0]
                            if start in station_list and end in station_list:
                                # Get indices of start and end stations
                                start_idx = station_list.index(start)
                                end_idx = station_list.index(end)
                                
                                # Determine direction (forward or reverse through station list)
                                if start_idx < end_idx:
                                    station_sequence = station_list[start_idx:end_idx + 1]
                                else:
                                    station_sequence = station_list[end_idx:start_idx + 1][::-1]
                                
                                # Create individual segments
                                for i in range(len(station_sequence) - 1):
                                    expanded_data.append(f"{cols[0]},{cols[1]},{cols[2]},{cols[3]},{cols[4]},{station_sequence[i]},{station_sequence[i+1]}")
                                break
        data = expanded_data
                    
        affected_lines = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                # convert to group names
                if cols[4] in ['Werribee', 'Williamstown','Frankston']:
                    group = 'cross_city'
                elif cols[4] in ['Lilydale','Belgrave','Alamein','Glen Waverley']:
                    group = 'burnley'
                elif cols[4] in ['Craigieburn','Upfield','Sunbury']:
                    group = 'northern'
                elif cols[4] in ['Pakenham','Cranbourne']:
                    group = 'dandenong'
                elif cols[4] in ['Sandringham']:
                    group = 'sandringham'
                elif cols[4] in ['Stony Point']:
                    group = 'stony_point'
                elif cols[4] in ['Hurstbridge', 'Mernda', 'City Circle']:
                    group = 'clifton_hill'
                elif cols[4] in ['Flemington Racecourse']:
                    group = 'flemington'
                elif cols[4] in ['Albury']:
                    group = 'standard_guage'
                elif cols[4] in ['Traralgon', 'Geelong','Bendigo','Seymour',]:
                    group = 'vline_intercity'
                elif cols[4] in ['Shepparton', 'Swan Hill', 'Echuca', 'Warrnambool', 'Bairnsdale']:
                    group = 'vline_long_distance'
                elif cols[4] in ['Ballarat']:
                    group = 'ballarat_seperate'
                elif cols[4] in ['Ararat', 'Maryborough']:
                    group = 'ararat/maryborough_seperate'
                else:
                    group = cols[4]
                    
                affected_lines.append((cols[5], cols[6], group))

        x_offset = x_offset_log_train_map_pre_munnel
        y_offset = y_offset_log_train_map_pre_munnel
        station_coordinates = station_coordinates_log_train_map_pre_munnel
        line_coordinates = lines_coordinates_log_train_map_pre_munnel
        
    # do the map gen
    map_handler = MapImageHandler(f"utils/trainlogger/map/{mode}", lines_dictionary, x_offset, y_offset, station_coordinates, line_coordinates)
    print(affected_lines)
    map_handler.highlight_map(affected_lines, f"temp/{user}.png", stations)