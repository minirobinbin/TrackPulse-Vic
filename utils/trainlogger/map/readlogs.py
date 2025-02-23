from utils.trainlogger.map.mapimage import MapImageHandler


def logMap(user:str, lines_dictionary:dict, mode:str='train'):
    if mode == 'train':
        file = open(f'utils/trainlogger/userdata/{user}.csv', 'r')
        data = file.readlines()
        file.close()

        stations = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
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
                start, end, group = cols[5], cols[6], cols[4]
                
                # Find the line that contains these stations
                for line_name, line_info in lines_dictionary.items():
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
            # convert to group names
            if cols[4] in ['Werribee', 'Williamstown','Frankston']:
                group = 'cross_city'
            elif cols[4] in ['Lilydale','Belgrave','Alamein','Glen Waverley']:
                group = 'burnley'
            elif cols[4] in ['Craigieburn','Upfield','Sunbury']:
                group = 'northern'
            elif cols[4] in ['Pakenham','Cranbourne']:
                group = 'dandenong'
            elif cols[4] in ['Flemington Racecourse']:
                group = 'flemington'
            elif cols[4] in ['Albury']:
                group = 'standard_guage'
                
            else:
                group = cols[4]
                
            cols = line.strip().split(',')
            if len(cols) >= 6:
                affected_lines.append((cols[5], cols[6], group))
        
        # do the map gen
        map_handler = MapImageHandler("utils/trainlogger/map/log_train_map.png", lines_dictionary)
        print(affected_lines)
        a = map_handler.highlight_map(affected_lines, "temp/themap.png", stations)