import requests
from datetime import date, timedelta
from flask import Flask, request, jsonify, redirect, url_for, request, flash 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import yaml
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
#creds = yaml.safe_load(open("creds.yaml", "r"))


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