'''

@app.route('/get_category_playlists')
def get_category_playlists():
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    category_id = 'dinner'  #replace with weather 
    limit = 10  #will get 10 songs 

    playlists_data = get_category_playlists_data(access_token, category_id, limit)
    return json.dumps(playlists_data, indent=2)

def get_category_playlists_data(access_token, category_id, limit):
    url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data
'''    
import os
from spotifyclient import SpotifyClient
import requests



weather_codes = ['','','','','']  #['sunny', 'snow', 'rain', 'rain', 'clear']

seed_track_bank = {  #list of seed-songs with spotify song ID's
    "sunny": "2RCkd4tms3VOEoTErKzInS", #Don't want to fall in love
    "overcast": "7FMedJPiag48GjON0tp2PO", #crane your neck
    "drizzle": "6iCJCZqDJjmBxt07Oid6FI", #buttercup 
    "rain": "72Q3BQhu0w6A81ouAUp7UL", #rain in june
    "snow": "6iCJCZqDJjmBxt07Oid6FI", #all i want for chistmas
    "thunderstrom": "73CMRj62VK8nUS4ezD2wvi" #set fire to the rain 
    }

#ID for seed track depending on weather code 
'''
rec_track = {}

for i in range(5):
    rec_track[i] = spotify_client.get_track_recommendations(seed_track_bank[weather_codes[i]])
'''

def get_song_recommendations(access_token, seed_tracks, limit=2):
    seed_tracks = ','.join(seed_tracks)
    url = f'https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data['tracks']

def add_tracks_to_playlist(access_token, playlist_id, track_ids):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    json_data = {
        'uris': [f'spotify:track:{track_id}' for track_id in track_ids]
    }
    response = requests.post(url, headers=headers, json=json_data)
    return response.status_code


#updated from the one from app.py
def create_playlist():
    name = "5 Day forecast " + d1
    public = 'true'
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    playlist = create_spotify_playlist(access_token, name, public)
    playlist_id = playlist["id"]

    for weather_code in weather_codes:
        seed_track = seed_track_bank[weather_code]
        recommended_songs = get_song_recommendations(access_token, [seed_track], limit=2)
        track_ids = [song['id'] for song in recommended_songs]
        add_tracks_to_playlist(access_token, playlist_id, track_ids)

    return json.dumps(playlist, indent=2)


