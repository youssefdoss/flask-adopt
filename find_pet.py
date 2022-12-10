'''Helper functions to aid in finding pets'''

import requests
from random import randint

DEFAULT_PHOTO_URL = 'https://www.ncenet.com/wp-content/uploads/2020/04/No-image-found.jpg'

def generate_oauth_token(PETFINDER_API_KEY, PETFINDER_API_SECRET):
    '''Generates an oauth token given api key and secret
    
    PETFINDER_API_KEY: string
    PETFINDER_API_SECRET: string
    
    returns: string'''

    d = {
        'grant_type': 'client_credentials',
        'client_id': PETFINDER_API_KEY,
        'client_secret': PETFINDER_API_SECRET
    }

    resp = requests.post(
        'https://api.petfinder.com/v2/oauth2/token',
        data=d
        )
    
    return resp.json()['access_token']

def get_random_pet(token):
    '''Returns a random pet name, age, and photo url
    
    token: string
    
    returns: dictionary'''

    resp = requests.get(
        'https://api.petfinder.com/v2/animals?limit=100',
        headers={"Authorization": f"Bearer {token}"}
    )

    resp = resp.json()
    breakpoint()

    index = randint(0, 99)

    name = resp['animals'][index]['name']
    age = resp['animals'][index]['age']
    try:
        photo_url = resp['animals'][index]['photos'][0]['small']
    except:
        photo_url = DEFAULT_PHOTO_URL
    
    return [name, age, photo_url]