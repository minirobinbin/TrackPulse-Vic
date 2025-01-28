# search for the station
from utils.search import search_api_request
from utils.stopid import find_stop_id


def nameToStopID(station, mode):
    Nstation = station.replace(' ', '%20').replace('#', '%23')
    if mode == "0":
        search = search_api_request(f'{Nstation.title()}%20Station')
    if mode == "3":
        search = search_api_request(f'{Nstation.title()}%20Railway%20Station')

    else:
        search = search_api_request(Nstation.title())
    # FIND STOP ID from search name
    try:
        if mode == "0":
            stop_id = find_stop_id(search, f"{station.title()} Station")
        elif mode == "3":
            stop_id = find_stop_id(search, f"{station.title()} Railway Station")
        else:
            print(f'searching for {station.title()}')
            stop_id = find_stop_id(search, f"{station.title()}")
    except:
        print(f"Cannot find id for {station.title()}")
        return 'None'
    print(f'STOP ID for {station} Station: {stop_id}')
    return stop_id