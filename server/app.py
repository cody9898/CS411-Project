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
#GOOGLE_MAPS_API_KEY = creds["GOOGLE_MAPS_API_KEY"]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    country = ''
    if request.method == 'POST':
        country = request.form.get('country')
        today = date.today()
        yesterday = today - timedelta(days=1)
        today = today.isoformat()
        yesterday = yesterday.isoformat()
        url = 'https://api.covid19api.com/country/{country}/status/confirmed?from={yesterday}&to={today}'.format(
            country=country,
            yesterday=yesterday,
            today=today
        )
        response = requests.get(url)
        results = response.json()
        try:
            result = results[0]
        except IndexError:
            result = {
                'Country': country,
                'Cases': 'no data'
            }
    response = requests.get('https://api.covid19api.com/countries')
    countries = response.json()
    return countries

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/search', methods=['GET'])
def search():

    results = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Sydney&key="+GOOGLE_MAPS_API_KEY)
    print("here")
    return jsonify(results)

# run app with command python app.py
if __name__ == '__main__':
    app.run()