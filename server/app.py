import requests
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml


app = Flask(__name__)

# Enable CORS support on all routes
cors = CORS(app)

# Get creds
#creds = yaml.safe_load(open("creds.yaml", "r"))


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

# run app with command python app.py
if __name__ == '__main__':
    app.run()