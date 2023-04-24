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

################################Test################################

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = 'cs460cs460'

app.config['MYSQL_DATABASE_PASSWORD'] = 'cs460cs460'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#conn = mysql.connect()
#cursor = conn.cursor()
#cursor.execute("SELECT email from Users")
#users = cursor.fetchall()
# connect to the GeoNames SQLite database
# configure the database path
'''
DATABASE = 'geonames.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    # retrieve a list of all countries from the database
    cursor = get_db().cursor()
    cursor.execute("SELECT DISTINCT country_name FROM geonames ORDER BY country_name")
    countries = cursor.fetchall()

    return render_template('index.html', countries=countries)

@app.route('/getCities', methods=['POST'])
def getCities():
    # retrieve the selected country from the request data
    country = request.form['country']

    # retrieve a list of all cities in the selected country
    cursor = get_db().cursor()
    cursor.execute("SELECT city_name, latitude, longitude FROM geonames WHERE country_name=?", (country,))
    cities = cursor.fetchall()

    # return the list of cities as a JSON response
    return {'cities': cities}
#@app.route('/getLocation', methods=['POST'])
#def getLocation():
    # get user's IP address
    #ip = request.remote_addr
    
    # call an external API to get the user's location from their IP address
    #response = requests.get('http://ip-api.com/json/'+ip)
    #data = response.json()
    
    # extract latitude and longitude from the response
    #lat = data['lat']
   # lon = data['lon']
    
    # return the location data as a string
    #return json.dumps(str(lat) + ',' + str(lon), indent=4, sort_keys=True)
'''
@app.route('/weather', methods=['POST'])
def get_tem(unit = 'fahrenheit'): #use boston location by default
    la = request.form.get('latitude')
    lo = request.form.get('longtitude')
    #url = f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&hourly=temperature_2m&temperature_unit={unit}"
    #api call:
    #response = requests.get(url)
    #retrieve the daily temperature forecast from the JSON response using dictionary indexing, and print it to the console
    #if response.status_code == 200:
        #data = response.json()
        #parsed = json.load(response.text)
        #pretty_json = json.dumps(response.json()['hourly']['temperature_2m'], indent=4, sort_keys=True)
        #hourly_data = data['hourly']['temperature_2m']
        #return pretty_json
    #else:
        #print(f"Error: {response.status_code}")
    wc = get_wc(la,lo)
    if wc is not None:
        m = json.dumps(wc, indent=4, sort_keys=True)
        return m
    else:
        return json.dumps("Oops, some errors occured", indent=4, sort_keys=True)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('hello.html', message='Logged out')



client_id = '961732832e4d40fb8d0f05531a1dbaf9'
#redirect_uri = 'http://localhost/5000/'
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)

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
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    })

    authorization_url = f'https://accounts.spotify.com/authorize?{args}'
    return redirect(authorization_url)

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
   
    user_profile_api_endpoint = "https://api.spotify.com/v1"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    print(profile_data)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        with open('access_token.txt', 'w') as f:
            f.write(access_token)
        return render_template("Hello.html")
    else:
        return f"Error: HTTP status {response.status_code}", 400
    
'''
@app.route('/profile')
def profile():
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    profile_data = get_profile(access_token)
    return json.dumps(profile_data, indent=2) #render_template("hello.html")  ############### problem area

def get_profile(access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data#render_template('hello.html')
'''
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

#default page
@app.route("/5000/", methods=['GET'])
def hello():
    return render_template('hello.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)