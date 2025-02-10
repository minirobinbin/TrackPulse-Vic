from datetime import datetime, timezone

def isPast(iso_time: str, end_time) -> bool:
    # Parse the ISO 8601 formatted time string
    date = datetime.fromisoformat(iso_time.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)

    # Check if the provided time is in the past
    return date <= end_time