import requests
import json

CLIENT_ID = 'bUgtHRd559o-'
CLIENT_SECRET = 'SANDBOX-I7jkXvidJiL4ruPmtHuT4JMlINe1gII1'


def get_public_token():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        'grant_type': 'client_credentials',
        'scope': 'public'
    }
    return requests.post('https://api.lyft.com/oauth/token', auth=client_auth, data=post_data)


def generate_authorization_url():
    return requests.get('https://api.lyft.com/oauth/authorize', params={
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'public rides.read rides.request',
        'state': 'payload'
    })


def get_user_token(authorization_code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code
    }
    return requests.post('https://api.lyft.com/oauth/token', auth=client_auth, data=post_data)


def get_eta(token, location):
    return requests.get('https://api.lyft.com/v1/eta', headers={
        'Authorization': 'Bearer ' + token.json()['access_token']
    }, params={
        'lat': location.json()['locations'][0]['feature']['geometry']['y'],
        'lng': location.json()['locations'][0]['feature']['geometry']['x']
    })


def get_cost(token, pickup_location, destination):
    return requests.get('https://api.lyft.com/v1/cost', headers={
        'Authorization': 'Bearer ' + token.json()['access_token']
    }, params={
        'start_lat': pickup_location.json()['locations'][0]['feature']['geometry']['y'],
        'start_lng': pickup_location.json()['locations'][0]['feature']['geometry']['x'],
        'end_lat': destination.json()['locations'][0]['feature']['geometry']['y'],
        'end_lng': destination.json()['locations'][0]['feature']['geometry']['x']
    })


def request_ride(token, pickup, destination, ride_type):
    parameters = {
        'ride_type': ride_type,
        'origin': pickup,
        'destination': destination,
    }
    print parameters
    return requests.post('https://api.lyft.com/v1/rides', headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }, data=json.dumps(parameters))
