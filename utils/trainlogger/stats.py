import csv
from collections import Counter

def topLines(user):
    with open(f'utils/trainlogger/userdata/{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line and station frequencies
        line_counter = Counter()
        station_counter = Counter()

        # Process each row in the CSV
        for row in reader:
            # Row format: TrainID, TrainType, Date, Line, Start, End
            # We are interested in columns 3, 4, and 5 (Line, Start, End)
            line = row[3]
            start_station = row[4]
            end_station = row[5]

            # Update counters
            line_counter.update([line])
            station_counter.update([start_station, end_station])

        # Get the 10 most common lines
        most_common_lines = line_counter.most_common(10)
        
        # Get the 10 most common stations
        most_common_stations = station_counter.most_common(10)

        # Prepare the results as a list
        results = []

        # Append the most common lines to the results list
        for line, count in most_common_lines:
            results.append(f"{line}: {count} times")

        # # Append the most common stations to the results list
        # results.append("\nThe 10 most frequent stations are:")
        # for station, count in most_common_stations:
        #     results.append(f"{station}: {count} times")
        print(results)
        return results
        
        
