from flask import Flask
from flask import request
from mako.template import Template
import mako.runtime
from utils import lyft
from utils import geo

mako.runtime.UNDEFINED = ''

app = Flask(__name__, static_url_path='')


@app.route('/')
def get_auth_url():
    template = Template(filename='templates/index.html')
    parameters = {
        'authorization_url': lyft.generate_authorization_url().url
    }
    return template.render(**parameters)


@app.route('/ride/')
def auth_success():
    template = Template(filename='templates/ride.html')
    lyft_user_token = lyft.get_user_token(request.args['code'])
    parameters = {
        'user_token': lyft_user_token
    }
    return template.render(**parameters)


@app.route('/request/', methods=['POST'])
def ride_request():
    template = Template(filename='templates/request.html')
    locations = request.form
    arcgis_token = geo.get_token()
    pickup_location = geo.geocode(arcgis_token, locations.getlist('pickup_location')[0])
    destination = geo.geocode(arcgis_token, locations.getlist('destination')[0])
    ride_type = locations.getlist('ride_type')[0]
    print pickup_location.json(), destination.json(), ride_type
    # lyft_user_token = lyft.get_user_token(request.args['code'])
    # ride = lyft.request_ride(lyft_user_token, pickup_location.json(), destination.json(), ride_type)
    # print ride.json()
    parameters = {

    }
    return template.render()


@app.route('/eta/')
def get_eta():
    template = Template(filename='templates/eta.html')
    arcgis_token = geo.get_token()
    locations = geo.geocode(arcgis_token, "Empire State Building")
    lyft_public_token = lyft.get_public_token()
    eta = lyft.get_eta(lyft_public_token, locations).json()
    parameters = {
        'location_address': locations.json()['locations'][0]['name'],
        'lyft_line_eta': eta['eta_estimates'][0]['eta_seconds'],
        'lyft_eta': eta['eta_estimates'][1]['eta_seconds'],
        'lyft_plus_eta': eta['eta_estimates'][2]['eta_seconds']
    }
    return template.render(**parameters)
