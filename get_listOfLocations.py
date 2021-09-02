import requests
#import threading

api_key = '5EwGXrez61sYdXlbdrlyeW6EISyx3DDZ9T0NxHZ5ucimTXzyZ7FTVDVzBMwvhx9S1ZQPrlphoAXjadiZQZp0CahlCy-QoV9IzWrvcSDgk885cCsSNsLLpDJsC1dHX3Yx'
endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % api_key}


def createList(location):

    parameters = {'term': '',
                  'location': location,
                  'categories': ["bars", "lounges", "beergardens", "clubcrawl", "danceclubs"],
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
