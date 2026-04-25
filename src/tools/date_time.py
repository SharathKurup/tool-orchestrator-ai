from datetime import datetime
from zoneinfo import ZoneInfo # Standard library in 3.9+
from timezonefinder import TimezoneFinder
from .location import get_location
from src.log_config import writeLog

def get_datetime(location=None):
    # Set a default 'now' to prevent UnboundLocalError
    now = datetime.now() 
    
    if location:
        writeLog(f"Getting datetime for location: {location}", "info")
        try:
            lat, lon = get_location(location)
            tf = TimezoneFinder()
            tz_name = tf.timezone_at(lng=lon, lat=lat)
            
            if tz_name:
                # Use ZoneInfo to get the actual time in that region
                now = datetime.now(ZoneInfo(tz_name))
                writeLog(f"Current time in {location} ({tz_name}): {now.strftime('%Y-%m-%d %H:%M:%S')}", "info")
            else:
                writeLog(f"Could not find timezone for coordinates: {lat}, {lon}", "warning")
        except Exception as e:
            writeLog(f"Error getting timezone for location '{location}': {e}", "error")        
    else:
        writeLog("Getting current local time", "info")
        now = datetime.now()

    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    writeLog(f"Current datetime: {date_time}", "info")
    return date_time
