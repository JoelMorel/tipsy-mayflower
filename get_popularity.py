from flask import Flask, render_template, request
from lib.LivePopularTimes import livepopulartimes

app = Flask(__name__)

# Set Up Vsariables
app_key = 'AIzaSyDeGaNjFcWO1efbZ4vxnQKcl5-H_6RQeCE'
proxy = 0

formatted_address_NYC = ['(Mamajuana Cafe Queens), 33-15 56th St, Queens, NY 11377', '(The Delancy), 168 Delancey St, New York, NY 10002', '(Yeras), 86-09 Northern Blvd, Jackson Heights, NY 11372', '(The Ainsworth Midtown), 45 E 33rd St, New York, NY 10016',
                         '(Banc Cafe), 431 3rd Ave, New York, NY 10016', '(The Gem Saloon), 375 3rd Ave, New York, NY 10016', '(230 Fifth Rooftop Bar), 230 5th Ave, New York, NY 10001', '(Pier 17), 89 South St, New York, NY 10038', '(Frying Pan), 207 12th Ave, New York, NY 10001']
formatted_address_AC = ['(The Pool After Dark), 777 Harrahs Blvd, Atlantic City, NJ 08401', '(Premier Nightclub), 1 Borgata Way, Atlantic City, NJ 08401', '(HQ2 Nightclub | Beachclub), 500 Boardwalk, Atlantic City, NJ 08401', '(DAER Nightclub), 1000 Boardwalk, Atlantic City, NJ 08401',
                        '(Anthem Lounge), 2801 Pacific Ave #303, Atlantic City, NJ 08401', '(Boogie Nights), 2831 Boardwalk, Atlantic City, NJ 08401', '(The Chelsea Beach Bar), 3001-3099, Boardwalk, Atlantic City, NJ 08401', '(Ballys Beach Bar), 1900 Boardwalk, Atlantic City, NJ 08401']
formatted_address_RVC = ['(Kaseys Kitchen & Cocktails), 23 N Park Ave, Rockville Centre, NY 11570', '(The New Vibe Lounge), 60 N Park Ave, Rockville Centre, NY 11570',
                         '(Croxleys Great American Ale House), 7 S Park Ave, Rockville Centre, NY 11570', '(Dark Horse Tavern), 12 S Park Ave, Rockville Centre, NY 11570']


def checkCityPopularity(cityName):
    responseData = {}

    if cityName == 'NYC':
        for i in formatted_address_NYC:
            response = livepopulartimes.get_populartimes_by_address(
                i, proxy=proxy)
            name = response['name']
            address = response['address']
            current_popularity = response['current_popularity']
            rating = response['rating']
            responseData[i] = dict(name=name, address=address,
                                   current_popularity=current_popularity, rating=rating)
        responseList = responseData.values()
        return responseList

    if cityName == 'AC':
        for i in formatted_address_AC:
            response = livepopulartimes.get_populartimes_by_address(
                i, proxy=proxy)
            name = response['name']
            address = response['address']
            current_popularity = response['current_popularity']
            rating = response['rating']
            responseData[i] = dict(name=name, address=address,
                                   current_popularity=current_popularity, rating=rating)
        responseList = responseData.values()
        return responseList

    if cityName == 'RVC':
        for i in formatted_address_RVC:
            response = livepopulartimes.get_populartimes_by_address(
                i, proxy=proxy)
            name = response['name']
            address = response['address']
            current_popularity = response['current_popularity']
            rating = response['rating']
            responseData[i] = dict(name=name, address=address,
                                   current_popularity=current_popularity, rating=rating)
        responseList = responseData.values()
        return responseList


app.route('/results')


def results():
    return render_template('results.html', city, response)
