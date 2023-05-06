######################### Weather Vibes #########################
####### created by Jue Han, Ming Hill, and Catherine Vess #######

import flask
from flask import Flask, Response, request, render_template, redirect, url_for, g
from flaskext.mysql import MySQL
import flask_login
import json
import requests
import os
import requests
import base64
import json
import random
import hashlib
from flask import Flask, request, redirect, url_for, render_template
from urllib.parse import urlencode, urlparse, parse_qs
from get_weathercode import get_wc
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from datetime import date

################################Test################################

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'shhitsasecret' 

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cs460cs460'
app.config['MYSQL_DATABASE_DB'] = 'weather'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#connect to MySQL
conn = mysql.connect()
cursor = conn.cursor()

#get the date
today = date.today()
d1 = today.strftime("%m-%d")
#print("d1 =", d1)
#print(str(d1))

seed_track_bank = {  #list of seed-songs with spotify song ID's
    "sunny": ["2RCkd4tms3VOEoTErKzInS","4sNG6zQBmtq7M8aeeKJRMQ","5euumi7eqEgmxvCIJw2pSp","5bzf1xrbqr1ttjAJuRz2xY"], #Don't want to fall in love + more
    "overcast": ["7FMedJPiag48GjON0tp2PO","1gcyHQpBQ1lfXGdhZmWrHP","4yugZvBYaoREkJKtbG08Qr","1K3LRUEcUz5FMtPYyg0F45"], #crane your neck + more
    "drizzle": ["6iCJCZqDJjmBxt07Oid6FI","7eqoqGkKwgOaWNNHx90uEZ","4U45aEWtQhrm8A5mxPaFZ7","75TDPu9k7Yv3IovdYaNCwk"], #buttercup + more
    "rain": ["72Q3BQhu0w6A81ouAUp7UL","2GiJYvgVaD2HtM8GqD9EgQ","4s6LhHAV5SEsOV0lC2tjvJ","77KnJc8o5G1eKVwX5ywMeZ" ],#rain in june + more
    "snow": ["6iCJCZqDJjmBxt07Oid6FI","2QjOHCTQ1Jl3zawyYOpxh6","7F5oktn5YOsR9eR5YsFtqb","5uPpzqixdzAMXprr4P5aT5"], #all i want for chistmas + more
    "thunderstorm": ["73CMRj62VK8nUS4ezD2wvi", "1eyzqe2QqGZUmfcPZtrIyt", "0hNhlwnzMLzZSlKGDCuHOo","0qUcpOOna3kkrwfqky85e1"] #set fire to the rain + more
    }

@app.route('/weather', methods=['POST']) #get lat, long, and cityname then get weather codes and then create_playlist + return template
def get_tem(unit = 'fahrenheit'): 
    cityName = request.form.get('city')
    limit = request.form["slider"]
    print("limit = "+ limit)
    if cityName != "":
        lat,long = get_lat_long(cityName)
    else:
        lat,long,cityName = get_current_location()
    wc,wcNum = get_wc(lat,long)
    if wc is not None:
        m = json.dumps(wc, indent=4, sort_keys=True)
        print(lat,long)
        translation = []
        imagelinks = []
        for p in range (len(wcNum)):
           string,link = get_wc_music(wcNum[p])
           translation.append(string)
           imagelinks.append(link)
        dump, playlist_uri,playlist_id = create_playlist(translation,cityName, limit)
        print(imagelinks)
        print(playlist_id)
        return render_template("weather.html",city=cityName, images = imagelinks, uri = playlist_uri, id = playlist_id)
    else:
        return json.dumps("Oops, some errors occured", indent=4, sort_keys=False)
    
def get_lat_long(city): #gets lat and long of city that was entered (based on a database)
    #convert it to lower cases, make it more efficient
    city = city.lower()
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(city, timeout=10)
        if location is None:
            return None
        else:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None
    
def get_current_location(): #gets users lat and long through ip2location API
    payload = {'key': 'AC734C7771F717B36767BB165121F669', 'ip': requests.get('https://api.ipify.org').text, 'format': 'json'}
    api_result = requests.get('https://api.ip2location.io/', params=payload)
    json_result = api_result.json()
    city = json_result['city_name']
    latitude = json_result['latitude']
    longitude = json_result['longitude']
    print(longitude, latitude, city)
    return latitude, longitude, city


def get_wc_music(wcNum): #converts weather codes to type of weather and returns weather + proper image to be displayed
    match wcNum:
        case 1 | 0:
            return ("sunny", 'images/Untitled_Artwork-1.png')

        case 2|3|45|48:
            return("overcast", 'images/Untitled_Artwork-3.png')

        case wcNum if 51 <= wcNum <=  57:
            return("drizzle", 'images/Untitled_Artwork-5.png')
        
        case wcNum if (61 <= wcNum <=  67) |  (81 <= wcNum <=  86):
            return("rain", 'images/Untitled_Artwork-6.png')

        case  wcNum if (71 <= wcNum <=  77)|wcNum==85|wcNum==86:
            return("snow", 'images/Untitled_Artwork-4.png')

        case wcNum if (95 <= wcNum <=  99):
            return("thunderstorm", 'images/Untitled_Artwork-7.png')

        case _:
            return("sunny", 'images/Untitled_Artwork-1.png')

def get_song_recommendations(access_token, seed_tracks, limit): #uses spotify API to gather recommendations based off of the seeds we entered 
    seed_tracks = ','.join(seed_tracks)
    url = f'https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data['tracks']

def add_tracks_to_playlist(access_token, playlist_id, track_ids): #adds the tracks spotify returned to the new playlist
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    json_data = {
        'uris': [f'spotify:track:{track_id}' for track_id in track_ids]
    }
    response = requests.post(url, headers=headers, json=json_data)
    return response.status_code


    
@app.route('/newsletter', methods=['POST']) #returns home page after newsletter has been entered and submits email to MySQL database
def uploadEmail():
    email = request.form.get('email')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO USERS (email) VALUES (%s)''', (email))
    conn.commit()
    return (render_template('hello.html'))


#important variables for spotify API
client_id = '961732832e4d40fb8d0f05531a1dbaf9'
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)


#additional functions for spotify API
def generate_random_string(length):
    s = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(length):
        s += random.choice(possible)
    return s

def sha256_digest(key):
    sha256 = hashlib.sha256()
    sha256.update(key)
    digest = sha256.digest()
    return digest

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def generate_code_challenge(code_verifier):
    data = code_verifier.encode('utf-8')
    digest = sha256_digest(data)
    return base64_url_encode(digest)

#Spotify authentication process
@app.route('/')
def authorize():
    print("AUTHORZING")
    code_verifier = generate_random_string(128)
    code_challenge = generate_code_challenge(code_verifier)
    state = generate_random_string(16)
    scope = 'user-top-read user-read-private user-read-email playlist-modify-public playlist-modify-private'

    with open('code_verifier.txt', 'w') as f:
        f.write(code_verifier)

    args = urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    })

    authorization_url = f'https://accounts.spotify.com/authorize?{args}'
    return redirect(authorization_url)

#get user information from authentication
@app.route('/callback/')
def callback():
    code = request.args.get('code')
    with open('code_verifier.txt', 'r') as f:
        code_verifier = f.read()

    body = urlencode({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'code_verifier': code_verifier
    })

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=body)

    response_data = json.loads(response.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
   
    user_profile_api_endpoint = "https://api.spotify.com/v1/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    print(profile_response)
    profile_data = json.loads(profile_response.text)
    with open('profile_data.txt', 'w') as f:
            f.write(json.dumps(profile_data))

    print(profile_data)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        with open('access_token.txt', 'w') as f:
            f.write(access_token)
        return render_template("Hello.html")
    else:
        return f"Error: HTTP status {response.status_code}", 400
    
#get users profile based off of the access token recieved  
def get_profile(access_token):
    code = request.args.get('code')
    with open('code_verifier.txt', 'r') as f:
        code_verifier = f.read()
        body = urlencode({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'code_verifier': code_verifier
    })
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=body)
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
     
    user_profile_api_endpoint = "https://api.spotify.com/v1"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    return profile_data

#create playlist and add songs to it through spotify API
@app.route('/create_playlist', methods=['POST'])
def create_playlist(weather_codes, city, limit):
    name = city+ " Forecast " + d1
    public = 'true'
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    playlist = create_spotify_playlist(access_token, name, public)
    playlist_id = playlist["id"]
    play_list_uri = playlist["uri"]
    print(play_list_uri)

    #convert weather codes to songs 
    for weather_code in weather_codes:
        seed_track = random.choice(tuple(seed_track_bank[weather_code]))
        recommended_songs = get_song_recommendations(access_token, [seed_track], limit)
        track_ids = [song['id'] for song in recommended_songs]
        add_tracks_to_playlist(access_token, playlist_id, track_ids)

    return json.dumps(playlist, indent=2),play_list_uri,playlist_id

#physical creation of the playlist
def create_spotify_playlist(access_token, name, public):
    with open('profile_data.txt') as f:
        profile_data = f.read()
    data = json.loads(profile_data)
    user_id = data['id']
    create_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    response = requests.post(
        create_playlist_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": name,
            "public": public
        }
    )

    json_resp = response.json()
    return json_resp


#default page
@app.route("/5000/", methods=['GET'])
def hello():
    return render_template('hello.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)