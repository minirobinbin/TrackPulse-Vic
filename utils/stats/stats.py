import os
import csv

def log_command(user_id, command_name):
    # Ensure the CSV file exists for the user
    file_path = f"utils/stats/data/{user_id}.csv"
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Command', 'Count'])

    # Read existing data
    existing_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                existing_data[row[0]] = int(row[1])
    
    # Update or add the command count
    current_count = existing_data.get(command_name, 0)
    existing_data[command_name] = current_count + 1

    # Write back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Command', 'Count'])  # Write header
        for command, count in existing_data.items():
            writer.writerow([command, count])
    print(f"Logged command {command_name} for user {user_id}")
    
def getFavoriteCommand(userid):
    command_usage = {}
    
    # Read the CSV file
    with open(f'utils/stats/data/{userid}.csv', mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            command = row['Command']
            count = int(row['Count'])
            command_usage[command] = count

    if not command_usage:
        return None, 0

    # Find the command with the highest count
    most_used = max(command_usage, key=command_usage.get)
    count = command_usage[most_used]

    return most_used, count