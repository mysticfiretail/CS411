import requests
#Boston location
latitude = 42.36
longitude = -71.06
unit = 'fahrenheit'
#url
url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&temperature_unit={unit}"
#api call:
response = requests.get(url)
#retrieve the daily temperature forecast from the JSON response using dictionary indexing, and print it to the console
def get_tem():
    if response.status_code == 200:
        data = response.json()
        hourly_data = data['hourly']['temperature_2m']
        return hourly_data
    else:
        print(f"Error: {response.status_code}")
