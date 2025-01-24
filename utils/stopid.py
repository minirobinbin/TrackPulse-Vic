# find the stop id!
def find_stop_id(data, location):
    for stop in data['stops']:
        if stop['stop_name'].strip() == location:
            return stop['stop_id']
    return 'None'