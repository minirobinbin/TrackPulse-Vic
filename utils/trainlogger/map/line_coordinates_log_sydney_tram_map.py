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
            (8900 + x_offset, 3750 + y_offset, 8900 + x_offset, 3900 + y_offset),
            (8900 + x_offset, 3800 + y_offset, 9750 + x_offset, 3890 + y_offset),
            (9700 + x_offset, 3800 + y_offset, 9800 + x_offset, 4000 + y_offset),
        ],
        ('Exhibition Centre', "Paddy's Markets"): [
            (8350 + x_offset, 3750 + y_offset, 8950 + x_offset, 3900 + y_offset),
        ],
        ('Convention', 'Exhibition Centre'): [
            (7750 + x_offset, 3750 + y_offset, 8400 + x_offset, 3900 + y_offset),
        ],
        ('Pyrmont Bay', 'Convention'): [
            (7150 + x_offset, 3750 + y_offset, 7800 + x_offset, 3900 + y_offset),
        ],
        ('John Street Square', 'Pyrmont Bay'): [
            (6550 + x_offset, 3750 + y_offset, 7200 + x_offset, 3900 + y_offset),
        ],
        ('Fish Market', 'John Street Square'): [
            (6000 + x_offset, 3750 + y_offset, 6600 + x_offset, 3900 + y_offset),
        ],
        ('Wentworth Park', 'Fish Market'): [
            (5400 + x_offset, 3750 + y_offset, 6050 + x_offset, 3900 + y_offset),
        ],
        ('Glebe', 'Wentworth Park'): [
            (4900 + x_offset, 3750 + y_offset, 5450 + x_offset, 3900 + y_offset),
        ],
        ('Jubilee Park', 'Glebe'): [
            (4450 + x_offset, 3750 + y_offset, 4950 + x_offset, 3900 + y_offset)
        ],
        ('Rozelle Bay', 'Jubilee Park'): [
            (4000 + x_offset, 3750 + y_offset, 4500 + x_offset, 3900 + y_offset),
        ],
        ('Lilyfield', 'Rozelle Bay'): [
            (3550 + x_offset, 3750 + y_offset, 4050 + x_offset, 3900 + y_offset),
        ],
        ('Leichardt North', 'Lilyfield'): [
            (3050 + x_offset, 3750 + y_offset, 3600 + x_offset, 3900 + y_offset),
        ],
        ('Hawthorne', 'Leichardt North'): [
            (2800 + x_offset, 3800 + y_offset, 2950 + x_offset, 4000 + y_offset),
            (2800 + x_offset, 3750 + y_offset, 3100 + x_offset, 3900 + y_offset),
        ],
        ('Marion', 'Hawthorne'): [
            (2800 + x_offset, 3950 + y_offset, 2900 + x_offset, 4250 + y_offset),
        ],
        ('Taveners Hill', 'Marion'): [
            (2800 + x_offset, 4200 + y_offset, 2950 + x_offset, 4500 + y_offset),
        ],
        ('Lewisham West', 'Taveners Hill'): [
            (2800 + x_offset, 4450 + y_offset, 2950 + x_offset, 4800 + y_offset),
        ],
        ('Waratah Mills', 'Lewisham West'): [
            (2800 + x_offset, 4750 + y_offset, 2950 + x_offset, 5100 + y_offset),
        ],
        ('Arlington', 'Waratah Mills'): [
            (2800 + x_offset, 5050 + y_offset, 2900 + x_offset, 5400 + y_offset),
        ],
        ('Dulwich Grove', 'Arlington'): [
            (2800 + x_offset, 5350 + y_offset, 2950 + x_offset, 5700 + y_offset),
        ],
        ('Dulwich Hill', 'Dulwich Grove'): [
            (2750 + x_offset, 5650 + y_offset, 2950 + x_offset, 5900 + y_offset),
        ],
    }
}