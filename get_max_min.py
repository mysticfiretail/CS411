import requests


def get_maxmin(la = 42.36,lo=-71.06, unit = 'fahrenheit'): #use boston location by default
    #url
    if unit == 'fahrenheit':
        url = f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York&temperature_unit={unit}"
    else:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York"
    #api call:
    response = requests.get(url)
    #retrieve the daily temperature forecast from the JSON response using dictionary indexing, and print it to the console
    if response.status_code == 200:
        data = response.json()
        ma = data['daily']['temperature_2m_max']
        mi = data['daily']['temperature_2m_min']
        return ma,mi
    else:
        print(f"Error: {response.status_code}")


print(get_maxmin())