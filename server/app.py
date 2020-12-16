import requests
from datetime import date, timedelta
from flask import Flask, request, jsonify, redirect, url_for, request, flash 
from flask_cors import CORS
import yaml
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
app = Flask(__name__)
#setting up the app

app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

#get database user model
#a user has an id, email, password, and name
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

# Enable CORS support on all routes
cors = CORS(app)

# Get creds
creds = yaml.safe_load(open("creds.yaml", "r"))
GOOGLE_MAPS_API_KEY = creds["GOOGLE_MAPS_API_KEY"]

# dictionary to convert state abbreviate to full state name 
state_abbr = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut",
"DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
"KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
"MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska",
"NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina",
"ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":
"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia",
"WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}


# algoritm to determine how dangerous a restaurant is, 0 is low danger and 10 is high danger 
def danger(state_nums, county_nums):
    ratio = county_nums/state_nums 
    if ratio > .50:
        return 10
    elif ratio > .45:
        return 9
    elif ratio > .40:
        return 8
    elif ratio > .35:
        return 7
    elif ratio > .30:
        return 6
    elif ratio > .25:
        return 5
    elif ratio > .20:
        return 4
    elif ratio > .15:
        return 3
    elif ratio > .10:
        return 2
    elif ratio > .05:
        return 1
    return 0
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return '' 

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/search', methods=['POST'])
def search():
    lat = request.form['lat']
    lng = request.form['lng']
    radius = request.form['radius']
    keyword = request.form['keyword']
    results = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(lng)+"&radius="+str(radius)+"&keyword="+keyword+"&key="+GOOGLE_MAPS_API_KEY)
    return jsonify(results.text)

@app.route('/info/<placeid>', methods=['GET'])
def info(placeid):

    # Uses Google Maps API to get address details of the restaurant
    # Process result and extract county and address
    results = (requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeid+"&key="+GOOGLE_MAPS_API_KEY))
    result_dictionary = json.loads(results.text)
    addresses = result_dictionary["result"]
    address_components = addresses["address_components"]
    county_temp = address_components[3]
    state_temp = address_components[4]
    county = county_temp["short_name"]
    county = county.split()[0]
    state = state_temp["long_name"]

    states_url = 'https://corona.lmao.ninja/v2/states/{state}'.format(
            state = state
        )

    # API to find covid data per county 
    counties_url = 'https://corona.lmao.ninja/v2/jhucsse/counties/{county}'.format(
        county = county
    )

    # get response from state url and convert the json to dictionary and find the value corresponding for number of cases
    state_response = requests.get(states_url)
    state_dict = json.loads(state_response.text)
    state_cases = state_dict["cases"]

    # get response from county url and convert json to dictionary, need to find index of correct county so match the 
    # state with each county to find the correct index of the county, once the county is found the stats of each county 
    # is in another dictionary. Find the amount of cases using another key
    counties_response = requests.get(counties_url)
    counties_dict = json.loads(counties_response.text)
    county_index = next((index for (index, d) in enumerate(counties_dict) if d["province"] == str(state)), None)
    specific_county = counties_dict[county_index]
    county_stats = specific_county["stats"]
    county_cases = county_stats["confirmed"]

    # get danger rating based off of state and county cases 
    rating = danger(state_cases,county_cases)

    # return state cases, county cases, and danger rating
    return str(state) + " cases: " + str(state_cases) + " " + str(county)+ " Cases: " + str(county_cases) + " " + "Danger Rating: " + str(rating)

@app.route('/coords_to_address', methods=['POST'])
def coordsToAddress():
    lat = request.form['lat']
    lng = request.form['lng']
    results = jsonify(requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key="+GOOGLE_MAPS_API_KEY).text)
    return results

@app.route('/address_to_coords', methods=['POST'])
def addressToCoords():
    # Specify address in accordance with  the format used by the national postal service of the country concerned.
    street = request.form['myStreet'].replace(" ", "+")
    city = ",+" + request.form['myCity'].replace(" ", "+")
    state = ",+" + request.form['myState'].replace(" ", "+")
    results = jsonify(requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+street+city+state+"&key="+GOOGLE_MAPS_API_KEY).text)
    return results
  
 @app.route('/profile', methods=['GET'])
def profile():
    return jsonify('profile')

@app.route('/logout')
def logout():
    return jsonify('logout')

@app.route('/login')
def login():
    return jsonify('login')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():  
    if request.method == 'POST': 
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        print(email, file=sys.stderr)
        return redirect('/')
    else:
        return jsonify ('signup')


    """user = User.query.filter_by(email=email).first() #if this returns a user then the email already exists in the batabase

    if user:
        flash('email address already exists')
        return redirect(url_for('/login'))

    new_user = User(email=email, name=name, password = generate_password_hash(password, method='sha256'))

        #adding new user to the database 
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('/profile'))  """    
    

# run app with command python app.py
if __name__ == '__main__':
    app.run()