from utils.trainlogger.map.mapimage import CoordinateFinder, CoordinateCorrector

answer = input("Type F for Finder, C for Corrector: ")
if answer == "F":
    finder = CoordinateFinder("utils/trainlogger/map/log_train_map.png")
    finder.run()
elif answer == "C":
    corrector = CoordinateCorrector("utils/trainlogger/map/log_train_map.png")
    corrector.run()
else:
    print("Syntax Error: Restart to try again")