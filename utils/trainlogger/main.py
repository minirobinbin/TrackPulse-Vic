import csv

def addTrain(username, date, train_number, line):
    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/{username}.csv"

    # Write the data to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, train_number, line])
    
    print(f"Data saved to {filename}")
    
import csv

def read_from_csv(username):
    # Create the filename based on the username
    filename = f"utils/trainlogger/userdata/{username}.csv"

    try:
        # Open the CSV file and read the data
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # Print the data
        if len(data) > 0:
            print(f"Data for {username}:")
            for row in data:
                print(row)
        else:
            print(f"No data found for {username}")
    except FileNotFoundError:
        print(f"File {filename} not found.")