from utils.trainlogger.map.station_coordinates_log_sydney_tram_map import x_offset, y_offset

line_coordinates = {
    'L1': {
        ('Capitol Square', 'Central'): [
            (9700 + x_offset, 3950 + y_offset, 9800 + x_offset, 4350 + y_offset),
            (9650 + x_offset, 4350 + y_offset, 9800 + x_offset, 4500 + y_offset), # Central Coords
            (9550 + x_offset, 4500 + y_offset, 9750 + x_offset, 4600 + y_offset), # Central Coords
            (9300 + x_offset, 4500 + y_offset, 9550 + x_offset, 4650 + y_offset), # Central Coords
        ],
        ("Paddy's Markets", 'Capitol Square'): [
            (8900 + x_offset, 3750 + y_offset, 8900 + x_offset, 3850 + y_offset),
            (8900 + x_offset, 3800 + y_offset, 9750 + x_offset, 3850 + y_offset),
            (9700 + x_offset, 3800 + y_offset, 9800 + x_offset, 4000 + y_offset),
        ],
        ('Exhibition Centre', "Paddy's Markets"): [
            (8350 + x_offset, 3750 + y_offset, 8950 + x_offset, 3850 + y_offset),
        ],
        ('Convention', 'Exhibition Centre'): [
            (7750 + x_offset, 3750 + y_offset, 8400 + x_offset, 3850 + y_offset),
        ],
        ('Pyrmont Bay', 'Convention'): [
            (7150 + x_offset, 3750 + y_offset, 7800 + x_offset, 3850 + y_offset),
        ],
        ('John Street Square', 'Pyrmont Bay'): [
            (6550 + x_offset, 3750 + y_offset, 7200 + x_offset, 3850 + y_offset),
        ],
        ('Fish Market', 'John Street Square'): [
            (6000 + x_offset, 3750 + y_offset, 6600 + x_offset, 3850 + y_offset),
        ],
        ('Wentworth Park', 'Fish Market'): [
            (5400 + x_offset, 3750 + y_offset, 6050 + x_offset, 3800 + y_offset),
        ],
        ('Glebe', 'Wentworth Park'): [
            (4900 + x_offset, 3750 + y_offset, 5450 + x_offset, 3850 + y_offset),
        ],
        ('Jubilee Park', 'Glebe'): [
            (4450 + x_offset, 3750 + y_offset, 4950 + x_offset, 3850 + y_offset)
        ],
        ('Rozelle Bay', 'Jubilee Park'): [
            (4000 + x_offset, 3750 + y_offset, 4500 + x_offset, 3850 + y_offset),
        ],
        ('Lilyfield', 'Rozelle Bay'): [
            (3550 + x_offset, 3750 + y_offset, 4050 + x_offset, 3850 + y_offset),
        ],
        ('Leichhardt North', 'Lilyfield'): [

        ],
        ('Hawthorne', 'Leichhardt North'): [

        ],
        ('Marion', 'Hawthorne'): [

        ],
        ('Taveners Hill', 'Marion'): [

        ],
        ('Lewisham West', 'Taveners Hill'): [

        ],
        ('Waratah Mills', 'Lewisham West'): [

        ],
        ('Arlington', 'Waratah Mills'): [

        ],
        ('Dulwich Grove', 'Arlington'): [

        ],
        ('Dulwich Hill', 'Dulwich Grove'): [

        ],
    }
}