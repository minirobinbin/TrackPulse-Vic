import csv
import os

def save_favourites(name, stop):
    filename = f"utils/favourites/data/{name}.csv"
    
    # Check if favourite already exists
    existing_favourites = get_favourites(name)
    if stop in existing_favourites:
        return f"{stop} is already in your favourites"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Write the string to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([stop])
    
    return f"Added {stop} to your favourite stops"

def remove_favourite(name, stop):
    filename = f"utils/favourites/data/{name}.csv"
    
    # Get current favourites
    favourites = get_favourites(name)
    if stop not in favourites:
        return f"{stop} is not in your favourites"
    
    # Remove the stop and write back to file
    favourites.remove(stop)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for fav in favourites:
            writer.writerow([fav])
    
    return f"Removed {stop} from your favourites"


        
def get_favourites(name):
    filename = f"utils/favourites/data/{name}.csv"
    favourites = []
    
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                favourites.append(row[0])
        return favourites
    except FileNotFoundError:
        return []