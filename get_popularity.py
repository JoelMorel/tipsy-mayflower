from flask import Flask, render_template, request
import get_listOfLocations
import livepopulartimes
# import threading

# Set Up Variables
app_key = 'EXAMPLEKEY'
proxy = 0


def checkCity(location):
    popularList, notPopularList = getList(location)
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
                categories = response['categories']
                latitude = response['coordinates']['lat']
                longitude = response['coordinates']['lng']
                popularData[i] = dict(name=name, address=address,
                                      current_popularity=current_popularity, rating=rating, cat=categories, lat=latitude, lng=longitude)
            else:
                name = response['name']
                print('Not popular: ' + name)
                address = response['address']
                current_popularity = response['current_popularity']
                rating = response['rating']
                categories = response['categories']
                notPopularData[i] = dict(name=name, address=address,
                                         current_popularity=current_popularity, rating=rating, cat=categories)
        except(IndexError, KeyError, TypeError):
            print('ERROR in call: ' + i)
    # print('popularData dict: ' + popularData)
    popularList = popularData.values()
    notPopularList = notPopularData.values()
    return popularList, notPopularList
