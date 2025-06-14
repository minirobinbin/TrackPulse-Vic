from utils.search import trainData
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import getTotalLines
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.lines_dictionaries import *
from utils.trainlogger.stats import getTotalTrips

print(getTotalTrips('all', 'all'))