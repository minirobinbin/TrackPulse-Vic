import csv
from collections import Counter
from datetime import datetime
from io import StringIO
from utils.trainlogger.stationDistance import *
from collections import Counter
import os

def topStats(user, stat):
    with open(f'utils/trainlogger/userdata/{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line and station frequencies
        line_counter = Counter()
        station_counter = Counter()
        set_counter = Counter()
        date_counter = Counter()
        type_counter = Counter()

        # Process each row in the CSV
        for row in reader:
            # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
            line = row[4]
            start_station = row[5]
            end_station = row[6]
            set = row[1]
            type = row[2]
            date = row[3]
            # Update counters
            line_counter.update([line])
            station_counter.update([start_station, end_station])
            set_counter.update([set])
            type_counter.update([type])
            date_counter.update([date])

        # Get the 10 most common lines
        most_common_lines = line_counter.most_common(100000)
        most_common_stations = station_counter.most_common(100000)
        most_common_sets = set_counter.most_common(100000)
        most_common_types = type_counter.most_common(100000)
        most_common_dates = date_counter.most_common(100000)

        # Get the 10 most common stations

        # Prepare the results as a list
        results = []
                
        # Append the most common lines to the results list
        if stat == "lines":
            for line, count in most_common_lines:
                results.append(f"{line}: {count} times")
        if stat == "stations":
            for station, count in most_common_stations:
                results.append(f"{station}: {count} times")
        if stat == "sets":
            for set, count in most_common_sets:
                results.append(f"{set}: {count} times")
        if stat == "types":
            for type, count in most_common_types:
                results.append(f"{type}: {count} times")
        if stat == "dates":
            for date, count in most_common_dates:
                results.append(f"{date}: {count} times")
        # # Append the most common stations to the results list
        # results.append("\nThe 10 most frequent stations are:")
        # for station, count in most_common_stations:
        #     results.append(f"{station}: {count} times")
        print(results)
        return results
    
# tram version
def tramTopStats(user, stat):
    with open(f'utils/trainlogger/userdata/tram/{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line and station frequencies
        line_counter = Counter()
        station_counter = Counter()
        set_counter = Counter()
        date_counter = Counter()
        type_counter = Counter()

        # Process each row in the CSV
        for row in reader:
            # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
            line = row[4]
            start_station = row[5]
            end_station = row[6]
            set = row[1]
            type = row[2]
            date = row[3]
            # Update counters
            line_counter.update([line])
            station_counter.update([start_station, end_station])
            set_counter.update([set])
            type_counter.update([type])
            date_counter.update([date])

        # Get the 10 most common lines
        most_common_lines = line_counter.most_common(100000)
        most_common_stations = station_counter.most_common(100000)
        most_common_sets = set_counter.most_common(100000)
        most_common_types = type_counter.most_common(100000)
        most_common_dates = date_counter.most_common(100000)

        # Get the 10 most common stations

        # Prepare the results as a list
        results = []
                
        # Append the most common lines to the results list
        if stat == "lines":
            for line, count in most_common_lines:
                results.append(f"{line}: {count} times")
        if stat == "stations":
            for station, count in most_common_stations:
                results.append(f"{station}: {count} times")
        if stat == "sets":
            for set, count in most_common_sets:
                results.append(f"{set}: {count} times")
        if stat == "types":
            for type, count in most_common_types:
                results.append(f"{type}: {count} times")
        if stat == "dates":
            for date, count in most_common_dates:
                results.append(f"{date}: {count} times")
        # # Append the most common stations to the results list
        # results.append("\nThe 10 most frequent stations are:")
        # for station, count in most_common_stations:
        #     results.append(f"{station}: {count} times")
        print(results)
        return results


# sydney train version
def sydneyTrainTopStats(user, stat):
    with open(f'utils/trainlogger/userdata/sydney-trains/{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line and station frequencies
        line_counter = Counter()
        station_counter = Counter()
        set_counter = Counter()
        date_counter = Counter()
        type_counter = Counter()

        # Process each row in the CSV
        for row in reader:
            # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
            line = row[4]
            start_station = row[5]
            end_station = row[6]
            set = row[1]
            type = row[2]
            date = row[3]
            # Update counters
            line_counter.update([line])
            station_counter.update([start_station, end_station])
            set_counter.update([set])
            type_counter.update([type])
            date_counter.update([date])

        # Get the 10 most common lines
        most_common_lines = line_counter.most_common(100000)
        most_common_stations = station_counter.most_common(100000)
        most_common_sets = set_counter.most_common(100000)
        most_common_types = type_counter.most_common(100000)
        most_common_dates = date_counter.most_common(100000)

        # Get the 10 most common stations

        # Prepare the results as a list
        results = []
                
        # Append the most common lines to the results list
        if stat == "lines":
            for line, count in most_common_lines:
                results.append(f"{line}: {count} times")
        if stat == "stations":
            for station, count in most_common_stations:
                results.append(f"{station}: {count} times")
        if stat == "sets":
            for set, count in most_common_sets:
                results.append(f"{set}: {count} times")
        if stat == "types":
            for type, count in most_common_types:
                results.append(f"{type}: {count} times")
        if stat == "dates":
            for date, count in most_common_dates:
                results.append(f"{date}: {count} times")
        # # Append the most common stations to the results list
        # results.append("\nThe 10 most frequent stations are:")
        # for station, count in most_common_stations:
        #     results.append(f"{station}: {count} times")
        print(results)
        return results

# sydney tram version
def sydneyTramTopStats(user, stat):
    with open(f'utils/trainlogger/userdata/sydney-trams/{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line and station frequencies
        line_counter = Counter()
        station_counter = Counter()
        set_counter = Counter()
        date_counter = Counter()
        type_counter = Counter()

        # Process each row in the CSV
        for row in reader:
            # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
            line = row[4]
            start_station = row[5]
            end_station = row[6]
            set = row[1]
            type = row[2]
            date = row[3]
            # Update counters
            line_counter.update([line])
            station_counter.update([start_station, end_station])
            set_counter.update([set])
            type_counter.update([type])
            date_counter.update([date])

        # Get the 10 most common lines
        most_common_lines = line_counter.most_common(100000)
        most_common_stations = station_counter.most_common(100000)
        most_common_sets = set_counter.most_common(100000)
        most_common_types = type_counter.most_common(100000)
        most_common_dates = date_counter.most_common(100000)

        # Get the 10 most common stations

        # Prepare the results as a list
        results = []
                
        # Append the most common lines to the results list
        if stat == "lines":
            for line, count in most_common_lines:
                results.append(f"{line}: {count} times")
        if stat == "stations":
            for station, count in most_common_stations:
                results.append(f"{station}: {count} times")
        if stat == "sets":
            for set, count in most_common_sets:
                results.append(f"{set}: {count} times")
        if stat == "types":
            for type, count in most_common_types:
                results.append(f"{type}: {count} times")
        if stat == "dates":
            for date, count in most_common_dates:
                results.append(f"{date}: {count} times")
        # # Append the most common stations to the results list
        # results.append("\nThe 10 most frequent stations are:")
        # for station, count in most_common_stations:
        #     results.append(f"{station}: {count} times")
        print(results)
        return results


def allTopStats(user, stat):
    file_pathsChecker = [
        f'utils/trainlogger/userdata/{user}.csv',
        f'utils/trainlogger/userdata/tram/{user}.csv',
        f'utils/trainlogger/userdata/sydney-trains/{user}.csv',
        f'utils/trainlogger/userdata/sydney-trams/{user}.csv'
    ]
    file_paths = [path for path in file_pathsChecker if os.path.exists(path)]

    # Counters to keep track of line and station frequencies
    line_counter = Counter()
    station_counter = Counter()
    set_counter = Counter()
    date_counter = Counter()
    type_counter = Counter()

    # Process each file in the list
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)

                # Process each row in the CSV
                for row in reader:
                    # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
                    line = row[4]
                    start_station = row[5]
                    end_station = row[6]
                    set = row[1]
                    type = row[2]
                    date = row[3]
                    # Update counters
                    line_counter.update([line])
                    station_counter.update([start_station, end_station])
                    set_counter.update([set])
                    type_counter.update([type])
                    date_counter.update([date])

    # Get the most common entries
    most_common_lines = line_counter.most_common(100000)
    most_common_stations = station_counter.most_common(100000)
    most_common_sets = set_counter.most_common(100000)
    most_common_types = type_counter.most_common(100000)
    most_common_dates = date_counter.most_common(100000)

    # Prepare the results as a list
    results = []

    # Append the most common entries to the results list based on the specified stat
    if stat == "lines":
        for line, count in most_common_lines:
            results.append(f"{line}: {count} times")
    elif stat == "stations":
        for station, count in most_common_stations:
            results.append(f"{station}: {count} times")
    elif stat == "sets":
        for set, count in most_common_sets:
            results.append(f"{set}: {count} times")
    elif stat == "types":
        for type, count in most_common_types:
            results.append(f"{type}: {count} times")
    elif stat == "dates":
        for date, count in most_common_dates:
            results.append(f"{date}: {count} times")
    print(results)
    return results 

def stationPercent(user):
    file = f'utils/trainlogger/userdata/{user}.csv'
    unique_items = set()
    
    # Read the CSV content
    reader = csv.reader(file.splitlines())
    
    for row in reader:
        # Extract the last two items from each row
        last_two_items = row[-2:]
        
        # Add each item to the set (sets only keep unique items)
        unique_items.update(last_two_items)
    
    # The number of unique items is the length of the set
    numberOfStations = 320
    
    total= len(unique_items)
    percent = round((total/numberOfStations)*100,2)
    return(f'{percent}%')

def linePercent(user):
    file = f'utils/trainlogger/userdata/{user}.csv'
    unique_items = set()
    
    # Read the CSV content
    with open(file, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            # Extract the fifth item from each row (index 4)
            fifth_item = row[4]
            
            # Add the item to the set (sets only keep unique items)
            unique_items.add(fifth_item)
    
    # The number of unique items is the length of the set
    numberOfLines = 22
    
    total = len(unique_items)
    percent = round((total / numberOfLines) * 100, 2)
    return f'{percent}%'

def lowestDate(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    # Initialize an empty list to store the dates
    dates = []

    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract the date string from each row and add it to the dates list
            dates.append(row[3])

    # Remove dashes from each date and convert them to integers
    cleaned_dates = [int(date.replace('-', '')) for date in dates]

    # Find the lowest number in the cleaned_dates list
    lowest_number = min(cleaned_dates)

    # Convert the lowest number back to the date format 'yyyy-mm-dd'
    lowest_date = str(lowest_number)[:4] + '-' + str(lowest_number)[4:6] + '-' + str(lowest_number)[6:]

    return lowest_date

def highestDate(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    # Initialize an empty list to store the dates
    dates = []

    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract the date string from each row and add it to the dates list
            dates.append(row[3])

    # Remove dashes from each date and convert them to integers
    cleaned_dates = [int(date.replace('-', '')) for date in dates]

    # Find the highest number in the cleaned_dates list
    highest_number = max(cleaned_dates)

    # Convert the highest number back to the date format 'yyyy-mm-dd'
    highest_date = str(highest_number)[:4] + '-' + str(highest_number)[4:6] + '-' + str(highest_number)[6:]

    return highest_date

def logAmounts(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = sum(1 for row in csv_reader)
    return line_count

def getTotalTravelDistance(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    distance = 0
    
    # Open and read the CSV file
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            col6 = row[5]
            col7 = row[6]
            try:
                distance += getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), col6, col7)
                print(f"{col6} to {col7}: {distance}")
            except:
                print(f'{col6} to {col7} could not be calculated!')
    
    return distance

def topOperators(user):
    metroTrains = ["X'Trapolis 100", "HCMT", 'EDI Comeng', 'Alstom Comeng', 'Siemens Nexas', "X'Trapolis 2.0"]
    vlineTrains = ['VLocity', 'N Class', 'Sprinter']
    
    sydneyTrainsLines = ['T1', 'T2', 'T3', "T4", 'T5', "T6", 'T7', 'T8', 'T9']
    nswTrainsLines = ['Blue Mountains Line', 'Central Coast & Newcastle Line', 'Hunter Line', "South Coast Line", 'Southern Highlands Line', "North Coast Region", 'North Western Region', 'Southern Region', 'Western Region']
    sydneyMetroLines = ['Metro North West Line',]
    
    metro_count = 0
    vline_count = 0
    yarra_trams_count=0
    sydney_trams_count=0

    sydney_trains_count=0
    nsw_trainlink_count=0
    sydney_metro_count=0
    other_count = 0
    try:
        with open(f'utils/trainlogger/userdata/{user}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                train_type = row[2]
                if train_type in metroTrains:
                    metro_count += 1
                elif train_type in vlineTrains:
                    vline_count += 1
                else:
                    other_count += 1
    except:
        pass
    
    # sydney trains
    try:
        with open(f'utils/trainlogger/userdata/sydney-trains/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                line = row[4]
                if line in sydneyTrainsLines:
                    sydney_trains_count +=1
                elif line in nswTrainsLines:
                    nsw_trainlink_count +=1
                elif line in sydneyMetroLines:
                    sydney_metro_count +=1
    except:
        pass
    
     # sydney tram
    try:
        with open(f'utils/trainlogger/userdata/sydney-trams/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                sydney_trams_count +=1
    except:
        pass    
    
    # melbourne tram
    try:
        with open(f'utils/trainlogger/userdata/tram/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yarra_trams_count +=1
    except:
        pass   
    # Write the results to a new CSV file
    output = f'temp/{user}TopOperators.csv'
    
    with open(output, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metro', metro_count])
        writer.writerow(['V/Line', vline_count])
        writer.writerow(['Sydney Trains', sydney_trains_count])
        writer.writerow(['NSW Trainlink', nsw_trainlink_count])
        writer.writerow(['Sydney Metro', sydney_metro_count])
        writer.writerow(['Yarra Trams', yarra_trams_count])
        writer.writerow(['Sydney Light Rail', sydney_trams_count])
        writer.writerow(['Other', other_count])
                
    return output

