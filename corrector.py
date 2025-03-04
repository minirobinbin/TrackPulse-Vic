from utils.trainlogger.map.mapimage import CoordinateCorrector
from utils.trainlogger.map.station_coordinates_log_train_map import x_offset, y_offset, station_coordinates
from utils.trainlogger.map.line_coordinates_log_train_map import line_coordinates

corrector = CoordinateCorrector("utils/trainlogger/map/log_train_map.png", x_offset, y_offset, station_coordinates, line_coordinates)
corrector.run()