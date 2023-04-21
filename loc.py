from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
#still not working, supposed to get geopy installed.
def get_location():
    try:
        geolocator = Nominatim(user_agent="my-application")
        ip_address = request.remote_addr  # get the user's IP address
        location = geolocator.geocode(ip_address)
        latitude = location.latitude
        longitude = location.longitude
        return (latitude, longitude)
    except GeocoderTimedOut:
        return None
m = get_location()