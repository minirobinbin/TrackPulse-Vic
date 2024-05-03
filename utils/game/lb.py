import pandas as pd
import csv
import os

def game():
    return("Chode!")



def addLb(username, id):
    csv_file = 'utils/game/leaderboard.csv'
    fieldnames = ['username', 'id', 'wins']
    data = []
    id_exists = False
    
    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file)
    
    if file_exists:
        # Read existing data into memory
        with open(csv_file, 'r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                data.append(row)
                if row['id'] == str(id):
                    # If the id exists, update 'wins' and mark id_exists as True
                    row['wins'] = str(int(row['wins']) + 1)
                    id_exists = True
    
    if not id_exists:
        # If id doesn't exist, add a new row with wins=1
        data.append({'username': username, 'id': id, 'wins': 1})
    
    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def top5():
    # Create an empty list to store (id, wins) tuples
    id_wins = []

    # Read the CSV file and populate the list with (id, wins) tuples
    with open('utils/game/leaderboard.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id_wins.append((row['id'], int(row['wins'])))

    # Sort the list of tuples by wins in descending order
    sorted_ids = sorted(id_wins, key=lambda x: x[1], reverse=True)

    # Get the top 5 (id, wins) tuples
    top_5_ids = sorted_ids[:5]

    return top_5_ids