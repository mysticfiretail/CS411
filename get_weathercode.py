import requests
weather_dict = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog and depositing rime fog',
    48: 'Fog and depositing rime fog',
    51: 'Drizzle: Light intensity',
    53: 'Drizzle: Moderate intensity',
    55: 'Drizzle: Dense intensity',
    56: 'Freezing Drizzle: Light intensity',
    57: 'Freezing Drizzle: Dense intensity',
    61: 'Rain: Slight intensity',
    63: 'Rain: Moderate intensity',
    65: 'Rain: Heavy intensity',
    66: 'Freezing Rain: Light intensity',
    67: 'Freezing Rain: Heavy intensity',
    71: 'Snow fall: Slight intensity',
    73: 'Snow fall: Moderate intensity',
    75: 'Snow fall: Heavy intensity',
    77: 'Snow grains',
    80: 'Rain showers: Slight intensity',
    81: 'Rain showers: Moderate intensity',
    82: 'Rain showers: Violent intensity',
    85: 'Snow showers: Slight intensity',
    86: 'Snow showers: Heavy intensity',
    95: 'Thunderstorm: Slight or moderate',
    96: 'Thunderstorm with hail: Slight intensity',
    99: 'Thunderstorm with hail: Heavy intensity'
}

def get_wc(la,lo, unit = 'fahrenheit'): #use boston location by default
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
        weathercodes = data['daily']['weathercode']
        print(weathercodes)
        n = []
        for x in weathercodes:
            n.append(weather_dict[x])
        return n,weathercodes
    else:
        print(f"Error: {response.status_code}")
