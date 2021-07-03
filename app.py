from flask import Flask, jsonify, request, render_template
import get_popularity
import json

tipsywallflower = Flask(__name__)


@tipsywallflower.route('/')
def index():
    return render_template('index.html')


@tipsywallflower.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            location = request.form['location']
            city = request.form['city']

            if city == '' and location == '':
                return render_template('index.html')
            if city != '' and location != '':
                city = ''
            if city != '' and location == '':
                location = city
            hotSpots, notHopSpots = get_popularity.checkCity(location)
            # serializedHotSpots = json.dumps(hotSpots)
            # print(hotSpots[0][0]['lat'])
            return render_template('results.html', location=location, spots=hotSpots, notHotSpots=notHopSpots)
    except(IndexError, KeyError, TypeError):
        print('ERROR in call: ')


if __name__ == '__main__':
    tipsywallflower.run(debug=True)
