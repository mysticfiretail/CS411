import os
import requests
import base64
import json
from flask import Flask, request, redirect

# Spotify API credentials
CLIENT_ID = '961732832e4d40fb8d0f05531a1dbaf9'
CLIENT_SECRET = '932d4693a5c940b69003ade79734f8d8'

# Spotify authorization endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Callback URL for your application
REDIRECT_URI = 'http://localhost:5000/callback'

# User authorization scopes
SCOPE = 'user-library-read'

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # Redirect the user to the Spotify authorization page
    auth_query_params = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'scope': SCOPE,
    }
    auth_url = AUTH_URL + '?' + urllib.parse.urlencode(auth_query_params)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Exchange the authorization code for an access token
    auth_code = request.args['code']
    auth_header = base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode('ascii')).decode('ascii')
    token_response = requests.post(
        TOKEN_URL,
        headers={
            'Authorization': 'Basic ' + auth_header,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': REDIRECT_URI,
        }
    )

    # Store the access token and refresh token in session
    token_data = token_response.json()
    session['access_token'] = token_data['access_token']
    session['refresh_token'] = token_data['refresh_token']

    # Redirect the user to the home page
    return redirect('/home')

@app.route('/home')
def home():
    # Make an authorized request to the Spotify API
    access_token = session['access_token']
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_data = response.json()
    return 'Welcome, ' + user_data['display_name']

if __name__ == '__main__':
    app.run(debug=True)
