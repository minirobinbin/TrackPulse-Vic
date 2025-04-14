import zipfile
import pandas as pd
import os

class GTFSSchedule:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.data = {
            '1': {}, # Regional Train
            '2': {}, # Metropolitan Train
            '3': {}, # Metropolitan Tram
            '4': {}, # Metropolitan Bus
            '5': {}, # Regional Coach
            '6': {}, # Regional Bus
            '10': {}, # Interstate
            '11': {} # SkyBus
        }

    def load_gtfs(self):
        """Load GTFS data from zip file into pandas DataFrames"""
        required_files = [
            'agency.txt',
            'stops.txt',
            'routes.txt',
            'trips.txt',
            'stop_times.txt',
            'calendar.txt'
        ]

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as main_zip:
                # Iterate through each transport mode folder
                for mode in self.data.keys():
                    mode_zip_name = f"{mode}/google_transit.zip"
                    if mode_zip_name not in main_zip.namelist():
                        print(f"Warning: {mode_zip_name} not found")
                        continue
                    
                    # Extract mode zip to memory and open it
                    mode_zip_data = main_zip.read(mode_zip_name)
                    with zipfile.ZipFile(pd.io.common.BytesIO(mode_zip_data)) as mode_zip:
                        # Read each GTFS file into a pandas DataFrame
                        for filename in required_files:
                            if filename in mode_zip.namelist():
                                with mode_zip.open(filename) as f:
                                    self.data[mode][filename.replace('.txt', '')] = pd.read_csv(f)
                            else:
                                print(f"Warning: {filename} not found in {mode}/google_transit.zip")

        except Exception as e:
            print(f"Error reading GTFS zip file: {e}")
            return None

    def get_schedule_for_stop(self, stop_id, mode):
        """Get schedule for a specific stop"""
        if mode not in self.data or 'stop_times' not in self.data[mode]:
            return None

        stop_times = self.data[mode]['stop_times']
        return stop_times[stop_times['stop_id'] == stop_id]

    def get_route_info(self, route_id, mode):
        """Get information about a specific route"""
        if mode not in self.data or 'routes' not in self.data[mode]:
            return None

        routes = self.data[mode]['routes']
        return routes[routes['route_id'] == route_id]

if __name__ == "__main__":
    gtfs = GTFSSchedule("D:\Billy\Downloads\gtfs.zip")
    gtfs.load_gtfs()
    
    print(gtfs.get_route_info("9", "2"))