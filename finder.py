from utils.trainlogger.map.mapimage import CoordinateFinder, CoordinateCorrector

answer = input("Type F for finder, C for corrector")
if answer == "F":
    finder = CoordinateFinder("utils/trainlogger/map/log_train_map.png")
    finder.run()
else:
    print("Syntax Error: Restart to try again")