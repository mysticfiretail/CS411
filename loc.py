from geopy.geocoders import Nominatim

def get_location():
    geolocator = Nominatim(user_agent="my-app/1.0")
    location = geolocator.geocode("your query here")
    return location
m = get_location()