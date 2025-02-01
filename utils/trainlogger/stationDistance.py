import pandas as pd

def load_station_data(csv_file):
    """
    Load station data from a CSV file into a pandas DataFrame.
    
    :param csv_file: Path to the CSV file.
    :return: DataFrame with station data.
    """
    return pd.read_csv(csv_file)

def getStationDistance(df, station1, station2):
    """
    Calculate the distance between two stations.
    
    :param df: DataFrame containing station data.
    :param station1: Name of the first station.
    :param station2: Name of the second station.
    :return: Distance between the two stations in kilometers.
    """
    try:
        km1 = df.loc[df['Station'] == station1, 'KM'].values[0]
        km2 = df.loc[df['Station'] == station2, 'KM'].values[0]
        if station1 != 'Flagstaff' and station1 != 'Melbourne Central' and station1 != 'Parliament' and station2 != 'Flagstaff' and station2 != 'Melbourne Central' and station2 != 'Parliament':
            return abs(km1 - km2)
        elif km1 <= 0 or km2 <= 0:
            return abs(km1 - km2)
        else:
            return abs(km1 + km2)
    except:
        return 'N/A'
