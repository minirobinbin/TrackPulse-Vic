import time
import datetime
import pytz


def convert_to_unix_time(date: datetime.datetime) -> str:
    # Get the end date
    end_date = date

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'

def convert_iso_to_unix_time(iso_time: str, format=None) -> str:
    if iso_time == "Skipped":
        return "Skipped"
    # Parse the ISO 8601 formatted time string
    date = datetime.datetime.fromisoformat(iso_time.replace('Z', '+00:00'))

    # Convert to the computer's current timezone
    date_local = date.astimezone()

    # Convert to Unix time
    unix_time = int(time.mktime(date_local.timetuple()))

    if format=='long-time':
        return f'<t:{unix_time}:T>'
    elif format=='short-time':
        return f'<t:{unix_time}:t>'
    else:
        # Format Unix time for Discord's timestamp
        return f'<t:{unix_time}:R>'
    

def convert_times(iso_time):
    # Replace 'Z' with '+0000' for UTC
    if iso_time.endswith('Z'):
        iso_time = iso_time[:-1] + '+0000'
    time_struct = time.strptime(iso_time, '%Y-%m-%dT%H:%M:%S%z')
    
    # Convert to Unix timestamp
    unix_time = int(time.mktime(time_struct))
    
    # Adjust for UTC if necessary (since mktime uses local time)
    if iso_time.endswith('+0000'):
        unix_time -= time.timezone  # Correct for UTC if local timezone is not UTC
    
    return unix_time

def unixTimeinXSeconds(seconds: int) -> str:
    return f'<t:{int(time.time()) + seconds}:R>'