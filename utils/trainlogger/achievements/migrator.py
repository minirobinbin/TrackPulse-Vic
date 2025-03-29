import os
import csv
from datetime import datetime

def is_date_like(string):
    """
    Check if a string resembles a date in 'YYYY-MM-DD' format or 'unknown'.
    """
    if string == 'unknown':
        return True
    try:
        datetime.strptime(string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def migrate_achievements_folder(folder_path):
    """
    Migrates all user achievement CSV files in the specified folder from the old format
    (list of IDs) to the new format (pairs of [id, date]) with 'unknown' as the date.
    
    Args:
        folder_path (str): Path to the folder containing user achievement CSV files.
    """
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist!")
        return
    
    migrated_count = 0
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            print(f"\nProcessing file: {file_path}")
            
            # Read the existing achievements
            existing_achievements = []
            try:
                with open(file_path, 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        existing_achievements = row  # Take the first row
                        break  # Assume single-row CSV
                print(f"Raw content: {existing_achievements}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
            
            if not existing_achievements:
                print(f"File {file_path} is empty. Skipping.")
                continue
            
            # Check if it's already in the new format
            # New format should have even length and every second element should be a date-like string
            is_new_format = (
                len(existing_achievements) % 2 == 0 and
                all(is_date_like(existing_achievements[i]) for i in range(1, len(existing_achievements), 2))
            )
            
            if is_new_format:
                print(f"File {file_path} is already in the new format. Skipping.")
                continue
            
            # Assume old format (list of IDs) and convert to new format
            new_achievements = []
            for achievement_id in existing_achievements:
                if achievement_id.strip():  # Skip empty strings
                    try:
                        # Validate that it's an ID (e.g., numeric string)
                        int(achievement_id)  # Assuming IDs are numeric
                        new_achievements.extend([achievement_id, 'unknown'])
                    except ValueError:
                        print(f"Warning: '{achievement_id}' in {file_path} doesn't look like a valid ID. Skipping this entry.")
            
            if not new_achievements:
                print(f"No valid achievements found in {file_path} to migrate. Skipping.")
                continue
            
            # Write the new format back to the file
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(new_achievements)
                print(f"Successfully migrated {file_path}. Achievements: {len(new_achievements) // 2}")
                migrated_count += 1
            except Exception as e:
                print(f"Error writing to {file_path}: {e}")
    
    print(f"\nMigration complete. {migrated_count} files migrated.")

# Example usage
if __name__ == "__main__":
    folder_path = 'utils/trainlogger/achievements/data'
    migrate_achievements_folder(folder_path)