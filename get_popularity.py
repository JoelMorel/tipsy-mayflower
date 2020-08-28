from flask import Flask, render_template, request
from LivePopularTimes import livepopulartimes
import get_listOfLocations

app = Flask(__name__)

# Set Up Vsariables
app_key = 'EXAMPLEKEY'
proxy = 0


def checkCity(location):
    # responseData = {}

    popularList, notPopularList = getList(location)
    # places = livepopulartimes.get_places_by_search("bars open in New York")
    # print(places)
    return popularList, notPopularList


def getList(location):
    popularData = {}
    notPopularData = {}

    listOfLocations = get_listOfLocations.createList(location)
    for i in listOfLocations:
        try:
            response = livepopulartimes.get_populartimes_by_address(
                i, proxy=proxy)
            if response['current_popularity'] != None:
                name = response['name']
                print('popular: ' + name)
                address = response['address']
                current_popularity = response['current_popularity']
                rating = response['rating']
                latitude = response['coordinates']['lat']
                longitude = response['coordinates']['lng']
                popularData[i] = dict(name=name, address=address,
                                      current_popularity=current_popularity, rating=rating, lat=latitude, lng=longitude)
            else:
                name = response['name']
                print('Not popular: ' + name)
                address = response['address']
                current_popularity = response['current_popularity']
                rating = response['rating']
                notPopularData[i] = dict(name=name, address=address,
                                         current_popularity=current_popularity, rating=rating)
        except(IndexError, KeyError, TypeError):
            print('ERROR in call: ' + i)
    popularList = popularData.values()
    notPopularList = notPopularData.values()
    return popularList, notPopularList
