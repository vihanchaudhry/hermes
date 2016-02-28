import mako.runtime
from flask import Flask
from flask import request
from mako.template import Template
import json
from utils import geo
from utils import lyft

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
        'user_token': lyft_user_token.json()['access_token']
    }
    return template.render(**parameters)


@app.route('/request/', methods=['POST'])
def ride_request():
    template = Template(filename='templates/request.html')
    locations = request.form
    arcgis_token = geo.get_token()
    pickup_location = geo.geocode(arcgis_token, locations.getlist('pickup_location')[0])
    destination = geo.geocode(arcgis_token, locations.getlist('destination')[0])
    orig_dict = {
        'lat': pickup_location.json()['locations'][0]['feature']['geometry']['y'],
        'lng': pickup_location.json()['locations'][0]['feature']['geometry']['x'],
        'address': pickup_location.json()['locations'][0]['name']
    }
    dest_dict = {
        'lat': destination.json()['locations'][0]['feature']['geometry']['y'],
        'lng': destination.json()['locations'][0]['feature']['geometry']['x'],
        'address': destination.json()['locations'][0]['name']
    }
    ride_type = locations.getlist('ride_type')[0]
    lyft_user_token = locations.getlist('user_token')[0]
    ride = lyft.request_ride(lyft_user_token, orig_dict, dest_dict, ride_type)
    print ride.json()
    parameters = {

    }
    return template.render()


@app.route('/eta/', methods=['POST'])
def get_eta():
    template = Template(filename='templates/eta.html')
    location = request.form
    arcgis_token = geo.get_token()
    pickup_location = geo.geocode(arcgis_token, location.getlist('pickup_location')[0])
    lyft_public_token = lyft.get_public_token()
    eta = lyft.get_eta(lyft_public_token, pickup_location).json()
    parameters = {
        'location_address': pickup_location.json()['locations'][0]['name'],
        'lyft_line_eta': eta['eta_estimates'][0]['eta_seconds'],
        'lyft_eta': eta['eta_estimates'][1]['eta_seconds'],
        'lyft_plus_eta': eta['eta_estimates'][2]['eta_seconds']
    }
    return template.render(**parameters)


@app.route('/etarequest/')
def get_eta_location():
    template = Template(filename='templates/etarequest.html')
    return template.render()


@app.route('/cost/', methods=['POST'])
def get_cost():
    template = Template(filename='templates/cost.html')
    locations = request.form
    arcgis_token = geo.get_token()
    pickup_location = geo.geocode(arcgis_token, locations.getlist('pickup_location')[0])
    destination = geo.geocode(arcgis_token, locations.getlist('destination')[0])
    lyft_public_token = lyft.get_public_token()
    cost = lyft.get_cost(lyft_public_token, pickup_location, destination).json()
    parameters = {
        'pickup_location': pickup_location.json()['locations'][0]['name'],
        'destination': destination.json()['locations'][0]['name'],
        'lyft_line_percentage': cost['cost_estimates'][0]['primetime_percentage'],
        'lyft_line_cost_max': cost['cost_estimates'][0]['estimated_cost_cents_max'] / 100,
        'lyft_line_cost_min': cost['cost_estimates'][0]['estimated_cost_cents_min'] / 100,
        'lyft_line_distance': cost['cost_estimates'][0]['estimated_distance_miles'],
        'lyft_line_duration': cost['cost_estimates'][0]['estimated_duration_seconds'] / 60,
        'lyft_percentage': cost['cost_estimates'][1]['primetime_percentage'],
        'lyft_cost_max': cost['cost_estimates'][1]['estimated_cost_cents_max'] / 100,
        'lyft_cost_min': cost['cost_estimates'][1]['estimated_cost_cents_min'] / 100,
        'lyft_distance': cost['cost_estimates'][1]['estimated_distance_miles'],
        'lyft_duration': cost['cost_estimates'][1]['estimated_duration_seconds'] / 60,
        'lyft_plus_percentage': cost['cost_estimates'][2]['primetime_percentage'],
        'lyft_plus_cost_max': cost['cost_estimates'][2]['estimated_cost_cents_max'] / 100,
        'lyft_plus_cost_min': cost['cost_estimates'][2]['estimated_cost_cents_min'] / 100,
        'lyft_plus_distance': cost['cost_estimates'][2]['estimated_distance_miles'],
        'lyft_plus_duration': cost['cost_estimates'][2]['estimated_duration_seconds'] / 60
    }
    return template.render(**parameters)


@app.route('/costrequest/')
def get_cost_locations():
    template = Template(filename='templates/costrequest.html')
    return template.render()
