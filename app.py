import flask
from flask import Flask, Response, request, render_template, redirect, url_for, g
from flaskext.mysql import MySQL
import flask_login
import json
import requests
from get_weathercode import get_wc
import sqlite3

#from loc import get_location

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Mysqlajue666'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#conn = mysql.connect()
#cursor = conn.cursor()
#cursor.execute("SELECT email from Users")
#users = cursor.fetchall()
# connect to the GeoNames SQLite database
# configure the database path
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


#default page
@app.route("/", methods=['GET'])
def hello():
    return render_template('hello.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
