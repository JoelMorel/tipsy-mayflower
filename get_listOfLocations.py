# url https://api.yelp.com/v3/businesses/search
import requests
api_key = 'gu4yF1nV3aomwzYAKYWMQ7H0mg-1ZpixLO-XgsvESWQqCIfSG2hUZIwEYLx42DzxPnEGdOS7t-qV0biZ3brXyObKdeu4o78tBINCgq2JuqE-MYiKY6mJ03ltQwY7X3Yx'
endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % api_key}


def createList(location):
    term = 'bars'
    # location = str(input('What is the address of the venue? '))

    parameters = {'term': term,
                  'location': location,
                  'categories': 'bars,clubs,nightlife'
                  }

    response = requests.get(url=endpoint, params=parameters, headers=headers)

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
    print(formatted_address)
    return formatted_address
