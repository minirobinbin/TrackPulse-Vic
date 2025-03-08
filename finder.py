from utils.trainlogger.map.mapimage import CoordinateFinder
from utils.trainlogger.map.station_coordinates_log_sydney_tram_map import x_offset, y_offset, station_coordinates
from utils.trainlogger.map.line_coordinates_log_sydney_tram_map import line_coordinates

finder = CoordinateFinder("utils/trainlogger/map/log_sydney-tram_map.png", x_offset, y_offset, station_coordinates, line_coordinates)
finder.run()