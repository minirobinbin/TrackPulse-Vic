import os
import csv
from tabnanny import check

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
    # end of line station checker
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
    