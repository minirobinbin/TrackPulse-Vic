import csv
import os
import uuid

def addTrain(username, date, train_number, train_type, line, start, end):
    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/{username}.csv"

    # Write the data to the CSV file
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, train_number,train_type, line, start, end])
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata')
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, train_number,train_type, line, start, end])

    print(f"Data saved to {filename}")

def readLogs(username):
    # Create the filename based on the username
    filename = f"utils/trainlogger/userdata/{username}.csv"
    user_data = []

    try:
        # Open the CSV file and read the data
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
        
        # Return the data instead of printing it
        if len(user_data) > 0:
            return user_data
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
        
def deleteRow(csv_file, row_number):
    with open(f'utils/trainlogger/userdata/{csv_file}', 'r') as file:
        rows = list(csv.reader(file))

    if row_number == 'last':
        row_number = len(rows) - 1
    if int(row_number) < 1 or int(row_number) >= len(rows):
        print("Invalid row number.")
        return

    del rows[int(row_number) - 1]

    with open(f'utils/trainlogger/userdata/{csv_file}', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Row {row_number} deleted successfully.")