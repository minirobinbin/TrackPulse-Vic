import csv
import os

def savelogin(username, password, id):
    # Create the directory if it doesn't exist
    os.makedirs('logins', exist_ok=True)
    
    with open(f'utils/myki/logins/{id}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the inputs as a new row in the CSV
        writer.writerow([username, password])

def readlogin(id):
    with open(f'utils/myki/logins/{id}.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            return row
