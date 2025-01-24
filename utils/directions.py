from utils.search import directionAPIrequest


def getDirectionName(direction_id):
    directionData = directionAPIrequest(direction_id)
    for direction in directionData['directions']:
        if str(direction['direction_id']) == str(direction_id):
            return direction['direction_name']