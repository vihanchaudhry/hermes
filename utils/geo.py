import requests


def get_token():
    return requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/', params={
        'f': 'json',
        'client_id': '5V24vfjL3LfcyKzR',
        'client_secret': 'a0c8bf7c2f444a83947ca1d0d60a86af',
        'grant_type': 'client_credentials',
        'expiration': '1440'
    })


def geocode(token, location):
    return requests.post('http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find', params={
        'f': 'json',
        'token': token.json()['access_token'],
        'text': location
    })
