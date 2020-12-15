import requests
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml


app = Flask(__name__)

# Enable CORS support on all routes
cors = CORS(app)

# Get creds
creds = yaml.safe_load(open("creds.yaml", "r"))
GOOGLE_MAPS_API_KEY = creds["GOOGLE_MAPS_API_KEY"]

state_abbr = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut",
"DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
"KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
"MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska",
"NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina",
"ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":
"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia",
"WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    state = ''
    county = ''
    if request.method == 'GET':
        # get county and state somehow 

        input_state_abr = 'SOME STATE ABBR'
        county = 'SOME COUNTY'

        state = state_abbr[input_state_abr]

        states_url = 'https://corona.lmao.ninja/v2/states/{state}'.format(
            state = state
        )
        counties_url = 'https://corona.lmao.ninja/v2/jhucsse/counties/{county}'.format(
            county = county
        )

        state_response = requests.get(states_url)
        counties_response = requests.get(counties_url)

        state_results = state_response.json()
        county_results = counties_response.json()
        try:
            state_result = state_results[0]
        except IndexError:
            result = {
                'State': state,
                'Cases': 'no data'
            }
        
    response = requests.get('https://api.covid19api.com/countries')
    countries = response.json()
    return countries

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
    results = jsonify(requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeid+"&key="+GOOGLE_MAPS_API_KEY).text)
    print(results["result"])
    return results

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
    

# run app with command python app.py
if __name__ == '__main__':
    app.run()