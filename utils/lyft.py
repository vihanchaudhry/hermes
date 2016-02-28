import requests

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
        'scope': 'public',
        'state': 'payload'
    })


def get_user_token(authorization_code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code
    }
    return requests.post('https://api.lyft.com/oauth/token', auth=client_auth, data=post_data)


def get_eta(token, locations):
    return requests.get('https://api.lyft.com/v1/eta', headers={
        'Authorization': 'Bearer ' + token.json()['access_token']
    }, params={
        'lat': locations.json()['locations'][0]['feature']['geometry']['y'],
        'lng': locations.json()['locations'][0]['feature']['geometry']['x']
    })


def request_ride(token, pickup, destination, ride_type):
    return requests.post('https://api.lyft.com/v1/rides', headers={
        'Authorization': 'Bearer ' + token.json()['access_token']
    }, params={
        'origin': pickup.json(),
        'destination': destination.json(),
        'ride_type': ride_type
    })
