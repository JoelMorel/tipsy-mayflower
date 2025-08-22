import os
import requests

endpoint = 'https://api.yelp.com/v3/businesses/search'


def createList(location, venue):
    api_key = os.environ.get('YELP_API_KEY')
    if not api_key:
        # Missing API key; fail gracefully
        return []
    headers = {'Authorization': f'bearer {api_key}'}

    parameters = {'term': venue,
                  'location': location,
                  'categories': venue,
                  'limit': 30,
                  'open_now': True,
                  }

    try:
        response = requests.get(
            url=endpoint, params=parameters, headers=headers)
        search_results = response.json()
        spots = search_results['businesses']
        formatted_address = []
        for spot in spots:
            name = spot['name']
            for key, value in spot['location'].items():
                if key == 'display_address':
                    if len(value) == 2:
                        new = value[0] + ', ' + value[1]
                    else:
                        new = value[0]+', ' + value[1] + ' ' + value[2]
                    together = f'({name}), {new}'

                    formatted_address.append(together)
    except(IndexError, KeyError, TypeError):
        print('ERROR in call: ')
    return formatted_address
