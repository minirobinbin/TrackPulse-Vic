from staticmap import StaticMap, Line
from typing import List, Tuple

# Function to convert string to list of coordinates
def parse_coordinates(paths: str) -> List[Tuple[float, float]]:
    return [tuple(map(float, coord.split(', '))) for coord in paths.split(' -')]

# Parse the path string into coordinates
coordinates = parse_coordinates(paths)

# Create a static map
m = StaticMap(600, 600, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

# Create a line from the coordinates
line = Line(coordinates, 'red', 2)

# Add line to the map
m.add_line(line)

# Save the map image
m.save('map_with_line.png')