from matplotlib.pylab import f
from utils.trainlogger.map.mapimage import MapImageHandler


def logMap(user:str, lines_dictionary:dict, mode:str='train', year:int=0):
    if mode == 'train':
        file = open(f'utils/trainlogger/userdata/{user}.csv', 'r')
        data = file.readlines()
        file.close()

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
                    
                    # Find the line that contains these stations
                    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Glen Waverley', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sunbury', 'Upfield'] and cols[5] in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'City Circle' and cols[5] in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'Frankston' and cols[5] in ['North Williamstown', 'Williamstown Beach', 'Williamstown']:
                        group = 'Williamstown'
                    elif group == 'Frankston' and cols[6] in ['North Williamstown', 'Williamstown Beach', 'Williamstown']:
                        group = 'Williamstown'
                    elif group == 'Frankston' and cols[5] in ['Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'Seaholme', 'Altona', 'Westona', 'Laverton', 'Aircraft', 'Williams Landing', 'Hoppers Crossing', 'Werribee']:
                        group = 'Werribee'
                    elif group == 'Frankston' and cols[6] in ['Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'Seaholme', 'Altona', 'Westona', 'Laverton', 'Aircraft', 'Williams Landing', 'Hoppers Crossing', 'Werribee']:
                        group = 'Werribee'
                    elif group == 'Bendigo' and 'Epsom' in [str(cols[5]), str(cols[6])]:
                        group = 'Epsom'
                    elif group == 'Bendigo' and 'Eaglehawk' in [str(cols[5]), str(cols[6])]:
                        group = 'Eaglehawk'
                    if group == 'Werribee' and cols[5] not in ['Seaholme', 'Altona', 'Westona'] and cols[6] not in ['Seaholme', 'Altona', 'Westona']:
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
        
        # do the map gen
        map_handler = MapImageHandler("utils/trainlogger/map/log_train_map.png", lines_dictionary)
        map_handler = MapImageHandler("utils/trainlogger/map/log_train_map.png", lines_dictionary)
        print(affected_lines)
        map_handler.highlight_map(affected_lines, f"temp/{user}.png", stations)