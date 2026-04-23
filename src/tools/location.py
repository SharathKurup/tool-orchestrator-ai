from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from src.logging import writeLog

def get_location(location_name):
    writeLog(f"Getting location for: {location_name}", "info")
    geolocator = Nominatim(user_agent="AI Tools", timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geocode(location_name)
    if location:
        writeLog(f"Location found for: {location_name}", "info")
        return location.latitude, location.longitude
    else:
        writeLog(f"Location not found: {location_name}", "error")
        raise ValueError(f"Could not find location: {location_name}")
    