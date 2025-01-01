import os
import csv

def manage_user_command(user_id, command_name):
    # Ensure the CSV file exists for the user
    file_path = f"{user_id}.csv"
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