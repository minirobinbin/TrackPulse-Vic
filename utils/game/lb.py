import pandas as pd
import csv
import os

def game():
    return("Chode!")



def addLb(username, id, game):
    print(f'adding {game}')

    csv_file = f'utils/game/scores/{game}.csv'
        
    fieldnames = ['username', 'id', 'wins', 'losses']
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
        data.append({'username': username, 'id': id, 'wins': 1, 'losses': 0})
    
    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def addLoss(username, id, game):
    csv_file = f'utils/game/scores/{game}.csv'
        
    fieldnames = ['username', 'id', 'wins', 'losses']
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
                    row['losses'] = str(int(row['losses']) + 1)
                    id_exists = True
    
    if not id_exists:
        # If id doesn't exist, add a new row with wins=1
        data.append({'username': username, 'id': id, 'losses': 1, 'wins': 0})
    
    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def top5(game):
    # Create an empty list to store (id, wins) tuples
    id_wins = []
    csv_file = f'utils/game/scores/{game}.csv'

    # Read the CSV file and populate the list with (id, wins) tuples
    try:
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_wins.append((row['username'], int(row['wins']), int(row['losses']),row['id'])) # username is actually id
    except FileNotFoundError:
        return 'no stats'
    
    # Sort the list of tuples by wins in descending order
    sorted_ids = sorted(id_wins, key=lambda x: x[1], reverse=True)

    # Get the top 5 (id, wins) tuples
    top_5_ids = sorted_ids[:10]

    return top_5_ids

def fetchUserStats(name):
    stats = []
    for game in ['guesser','ultrahard','domino','hangman']:
        csv_file = f'utils/game/scores/{game}.csv'
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                found = False
                for row in reader:
                    if row['id'] == name:
                        stats.append([row['id'], int(row['wins']), int(row['losses'])])
                        print(stats)
                        found = True
                if not found:
                    stats.append('no stats')
        except FileNotFoundError:
            stats.append('no stats')
    return stats