from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import get_popularity
import mysql.connector
app = Flask(__name__)

ENV = 'dev'
proxy = 0

if ENV == 'dev':
    app.env = 'dev'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
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
        return render_template('results.html', location=location, spots=hotSpots, notHotSpots=notHopSpots)


if __name__ == '__main__':
    app.run()
