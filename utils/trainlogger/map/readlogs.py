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
                    
        affected_lines = []
        for line in data:
            # convert to group names
            if cols[4] in ['Werribee', 'Williamstown','Frankston']:
                group = 'cross_city'
            elif cols[4] in ['Lilydale','Belgrave','Alamein','Glen Waverley']:
                group = 'burnley'
                
            else:
                group = cols[4]
                
            cols = line.strip().split(',')
            if len(cols) >= 6:
                affected_lines.append((cols[5], cols[6], group))
        
        map_handler = MapImageHandler("utils/trainlogger/map/log_train_map.png", lines_dictionary)
        print(affected_lines)
        a = map_handler.highlight_map(affected_lines, "temp/themap.png", stations)

        # print(stations)
    

