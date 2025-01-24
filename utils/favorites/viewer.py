import csv
import os

def save_favorites(name, stop):
    filename = f"utils/favorites/data/{name}.csv"
    
    # Check if favorite already exists
    existing_favorites = get_favorites(name)
    if stop in existing_favorites:
        return f"{stop} is already in your favorites"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Write the string to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([stop])
    
    return f"Added {stop} to your favorite stops"

def remove_favorite(name, stop):
    filename = f"utils/favorites/data/{name}.csv"
    
    # Get current favorites
    favorites = get_favorites(name)
    if stop not in favorites:
        return f"{stop} is not in your favorites"
    
    # Remove the stop and write back to file
    favorites.remove(stop)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for fav in favorites:
            writer.writerow([fav])
    
    return f"Removed {stop} from your favorites"


        
def get_favorites(name):
    filename = f"utils/favorites/data/{name}.csv"
    favorites = []
    
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                favorites.append(row[0])
        return favorites
    except FileNotFoundError:
        return []