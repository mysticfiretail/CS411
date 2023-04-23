from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
#If you get geopy installed, this will return you the latitude and longitude.
#Just use pip install geopy, it will work!!
def get_lat_long(city):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(city, timeout=10)
        if location is None:
            return None
        else:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None
