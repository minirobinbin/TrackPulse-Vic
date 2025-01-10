import os
import csv
from tabnanny import check
from datetime import datetime, timedelta

def checkAchievements(user):
    print('checking for first log...')
    new_achievements = []
    
    # first log checker
    filepath = f"utils/trainlogger/userdata/{user}.csv"

    if os.path.exists(filepath):
        new_achievements.append('1')
        print('First log achievement added')
    else:
        print('First log achievement not added')
    
    # all metro trains checker
    print('checking for all metro trains...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        mtrains = ["X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', 'HCMT']
        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[2]  
                if item in mtrains:
                    items_found.add(item)
        
        if items_found == set(mtrains):
            new_achievements.append('2')
            print('All Metro trains achievement added')
        else:
            print('All Metro trains achievement not added')
            print(f"Items missing: {set(mtrains) - items_found}")
            
    # all vline trains checker
    print('Checking for all v/line trains...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        mtrains = ["VLocity", 'N Class', 'Sprinter',]
        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[2]  
                if item in mtrains:
                    items_found.add(item)
        
        if items_found == set(mtrains):
            new_achievements.append('3')
            print('All V/Line trains achievement added')
        else:
            print('All V/Line trains achievement not added')
            print(f"Items missing: {set(mtrains) - items_found}")
            
    # all lines  checker
    print('Checking for all lines...')
    items_found = set()
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        mtrains = ["Lilydale", 'Belgrave', 'Alamein',"Glen Waverley", 'Bairnsdale', 'Traralgon', 'Pakenham', 'Cranbourne', 'Frankston', 'Stony Point', 'Sandringham', 'Williamstown', 'Werribee', 'Geelong', 'Warrnambool', 'Ballarat', 'Ararat', 'Marybourough', 'Swan Hill', 'Echuca', 'Bendigo', 'Seymour', 'Sunbury', 'Craigieburn', 'Upfield', 'Shepparton', 'Albury', 'Mernda', 'Hurstbridge']
        
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 1: 
                item = row[4]  
                if item in mtrains:
                    items_found.add(item)
        
        if items_found == set(mtrains):
            new_achievements.append('3')
            print('All lines achievement added')
        else:
            print('All lines achievement not added')
            print(f"Items missing: {set(mtrains) - items_found}")
            
    # 10 trips in a day checker
    print('Checking for 10 trips in a day...')
    dates = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 3:  # Make sure row has enough columns
                date = row[3]  # Date is in column 4
                dates[date] = dates.get(date, 0) + 1
        
        # Check if any date has 10 or more trips
        if any(count >= 10 for count in dates.values()):
            new_achievements.append('5')
            print('10 trips in a day achievement added')
        else:
            print('10 trips in a day achievement not added')
            print(f"Maximum trips in a day: {max(dates.values()) if dates else 0}")
        
    # end of line checker
    print('Checking for end of line stations...')
    end_stations = {
        'Lilydale', 'Belgrave', 'Alamein', 'Glen Waverley', 'East Pakenham', 'Cranbourne', 
        'Frankston', 'Stony Point', 'Sandringham', 'Williamstown', 'Werribee', 'Sunbury', 
        'Craigieburn', 'Upfield', 'Mernda', 'Hurstbridge', 'Warrnambool', 'Bairnsdale', 'Swan Hill', 'Echuca', 'Albury', 'Shepparton', 'Ararat', 'Maryborough'
    }

    visited_stations = set()
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 5:  # Make sure row has enough columns
                visited_stations.add(row[5])  # From station
                visited_stations.add(row[6])  # To station

        # Check if user has visited any end stations
        if any(station in end_stations for station in visited_stations):
            new_achievements.append('7')
            print('End of line achievement added')
        else:
            print('End of line achievement not added')
            print(f"End stations visited: {visited_stations & end_stations}")
            
    # 1 year of logging checker
    print('Checking for 1 year of logging...')

    oldest_date = None
    newest_date = None

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            if len(row) > 3:  # Make sure row has enough columns
                try:
                    date = datetime.strptime(row[3], '%Y-%m-%d')
                    if oldest_date is None or date < oldest_date:
                        oldest_date = date
                    if newest_date is None or date > newest_date:
                        newest_date = date
                except ValueError:
                    continue

    if oldest_date and newest_date:
        time_diff = newest_date - oldest_date
        if time_diff >= timedelta(days=365):
            new_achievements.append('11')
            print('1 year of logging achievement added')
        else:
            print('1 year of logging achievement not added')
            print(f"Current logging duration: {time_diff.days} days")
            
    # Check for log count achievements
    print('Checking for log count achievements...')
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        log_count = sum(1 for row in csv.reader(csvfile))
        
        if log_count >= 1000:
            new_achievements.extend(['12', '13', '14'])
            print('1000 logs achievement added')
        elif log_count >= 500:
            new_achievements.extend(['12', '13'])
            print('500 logs achievement added')
        elif log_count >= 100:
            new_achievements.append('12')
            print('100 logs achievement added')
        
        print(f"Current log count: {log_count}")
        
    # Check for Aboriginal train set numbers
    print('Checking for Aboriginal train sets...')
    special_sets = ['853M-1627T-854M', '933M-1667T-934M', '9024-9124-9224-9324-9724-9824-9924']

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] in special_sets:
                new_achievements.append('9')
                print('Aboriginal train set achievement added')
                break
        else:
            print('Aboriginal train set achievement not added')
            
    # Check for V/Line trains at Metro stations achievement
    print('Checking for V/Line trains at Metro stations...')
    vline_trains = {'Sprinter', 'VLocity', 'N Class'}
    metro_stations = {'Pakenham', 'Sunbury'}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:  # Ensure row has enough columns
                train_type = row[2]
                from_station = row[5]
                to_station = row[6]
                if (train_type in vline_trains and 
                    (from_station in metro_stations or to_station in metro_stations)):
                    new_achievements.append('16')
                    print('V/Line at Metro stations achievement added')
                    break
        else:
            print('V/Line at Metro stations achievement not added')
            
    # Check for SG trains
    print('Checking for SG trains...')
    pride_sets = ['1193-1593-1293', '1194-1594-1294', '1195-1595-1295', '1196-1596-1296', '1197-1597-1297']

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] in pride_sets:
                new_achievements.append('17')
                print('SG set achievement added')
                break
        else:
            print('SG set achievement not added')
    
    # Check for 7005 train
    print('Checking for the 7005 train...')
    vline_train_7005 = '7005'

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1 and row[1] == vline_train_7005:
                new_achievements.append('18')
                print('7005 train achievement added')
                break
        else:
            print('7005 train achievement not added')
            
    # Check for heratige train types
    print('Checking for heratige train types...')
    standard_trains = {'X\'Trapolis 100', 'X\'Trapolis 2.0', 'Alstom Comeng', 'EDI Comeng', 'HCMT', 
                      'Siemens Nexas', 'VLocity', 'Sprinter', 'N Class'}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 2 and row[2] not in standard_trains:
                new_achievements.append('8')
                print('heratige train achievement added')
                break
        else:
            print('heratige train achievement not added')
            
    # Check for 100 visits to a single station
    print('Checking for 100 visits to a single station...')
    station_visits = {}

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 6:
                from_station = row[5]
                to_station = row[6]
                station_visits[from_station] = station_visits.get(from_station, 0) + 1
                station_visits[to_station] = station_visits.get(to_station, 0) + 1
        
        if any(visits >= 100 for visits in station_visits.values()):
            new_achievements.append('19')
            print('100 visits to a single station achievement added')
        else:
            print('100 visits to a single station achievement not added')
            print(f"Most visited station count: {max(station_visits.values()) if station_visits else 0}")
    
    # Check for trains running on unusual lines
    print('Checking for trains running on unusual lines...')
    line_train_map = {
        'Lilydale': ["X'Trapolis 100"], 'Belgrave': ["X'Trapolis 100"], 'Alamein': ["X'Trapolis 100"], 
        'Glen Waverley': ["X'Trapolis 100"], 'Hurstbridge': ["X'Trapolis 100"], 'Mernda': ["X'Trapolis 100"], 
        'Pakenham': ['HCMT'], 'Cranbourne': ['HCMT'], 
        'Frankston': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Werribee': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Williamstown': ["X'Trapolis 100", "X'Trapolis 2.0", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'], 
        'Sandringham': ['Siemens Nexas', 'Alstom Comeng', 'EDI Comeng'], 
        'Upfield': ['Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"], 
        'Craigieburn': ['Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"], 
        'Sunbury': ['HCMT', 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas']
    }

    unusual_trains_found = False

    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 4:
                train_type = row[2]
                line = row[4]
                if line in line_train_map and train_type in line_train_map[line]:
                    continue
                elif line in line_train_map and train_type not in line_train_map[line]:
                    new_achievements.append('15')
                    unusual_trains_found = True
                    print(f'Unusual train {train_type} on line {line} achievement added')
                    break

    if not unusual_trains_found:
        print('Unusual train on line achievement not added')
        
    # Check for all stations visited
    print('Checking for all stations visited...')
    stations_visited = set()

    # Read all stations from the file
    all_stations = set()
    try:
        with open('utils/datalists/stations.txt', 'r', encoding='utf-8') as f:
            all_stations = {line.strip() for line in f if line.strip()}

        # Read visited stations from user data
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) > 6:
                    stations_visited.add(row[5])  # From station
                    stations_visited.add(row[6])  # To station

        if stations_visited.issuperset(all_stations):
            new_achievements.append('10')
            print('All stations achievement added')
        else:
            print('All stations achievement not added')
            print(f"Stations missing: {all_stations - stations_visited}")
    except FileNotFoundError:
        print('Stations list file not found')
    
    # check which achievements are actually new
    userCSV = f'utils/trainlogger/achievements/data/{user}.csv'
    existing_achievements = []
    
    if os.path.exists(userCSV):
        with open(userCSV, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_achievements.extend(row)
    
    truly_new = [ach for ach in new_achievements if ach not in existing_achievements]
    
    # update the user's achievements file
    if truly_new:
        all_achievements = existing_achievements + truly_new
        with open(userCSV, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(all_achievements)
        print(f"Added the following achievements: {truly_new}")
    else:
        print("No new achievements to add.")
    
    return truly_new


def returnAchievements(user):
    filepath = f'utils/trainlogger/achievements/data/{user}.csv'
    achievements = []

    # Read user's achievements
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                achievements.extend(row)

    # Get achievement details from master list
    achievement_details = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] in achievements:
                achievement_details.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                })

    return achievement_details

def getAchievementInfo(id):
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == id:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                }
        return None
    