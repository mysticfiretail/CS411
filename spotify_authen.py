import os
import requests
import base64
import json
import random
import hashlib
from flask import Flask, request, redirect, url_for, render_template
from urllib.parse import urlencode, urlparse, parse_qs

app = Flask(__name__)

client_id = '961732832e4d40fb8d0f05531a1dbaf9'
redirect_uri = 'http://localhost/'

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

@app.route('/')
def authorize():
    code_verifier = generate_random_string(128)
    code_challenge = generate_code_challenge(code_verifier)
    state = generate_random_string(16)
    scope = 'user-read-private user-read-email'

    with open('code_verifier.txt', 'w') as f:
        f.write(code_verifier)

    args = urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    })

    authorization_url = f'https://accounts.spotify.com/authorize?{args}'
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    with open('code_verifier.txt', 'r') as f:
        code_verifier = f.read()

    body = urlencode({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'code_verifier': code_verifier
    })

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        with open('access_token.txt', 'w') as f:
            f.write(access_token)
        return redirect(url_for('profile'))
    else:
        return f"Error: HTTP status {response.status_code}", 400

@app.route('/profile')
def profile():
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    profile_data = get_profile(access_token)
    return json.dumps(profile_data, indent=2)

def get_profile(access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    name = request.form.get('name')
    public = request.form.get('public', 'true').lower() == 'true'
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    playlist = create_spotify_playlist(access_token, name, public)
    return json.dumps(playlist, indent=2)

def create_spotify_playlist(access_token, name, public):
    me_data = get_profile(access_token)
    user_id = me_data['id']
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

if __name__ == '__main__':
    app.run(debug=True)