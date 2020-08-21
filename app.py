from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from LivePopularTimes import livepopulartimes
import get_popularity
import mysql.connector
app = Flask(__name__)

ENV = 'dev'
proxy = 0
city = ''

if ENV == 'dev':
    app.env = 'dev'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mysql:root@127.0.0.1/tipsy-wallflower'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ledia1lyvd5ncahd:n8x650vva6u3z1mo@arfo8ynm6olw6vpn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/m4q3e12uaejpc9ld'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db = mysql.connector.connect(
    host='arfo8ynm6olw6vpn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com	',
    user='ledia1lyvd5ncahd',
    password='n8x650vva6u3z1mo',
    port='3306',
    database='m4q3e12uaejpc9ld',
)


# class location(db.Model):
#     __tablename__ = 'location'
#     id = db.column(db.Integer, primary_key=True)
#     name = db.column(db.String(200), unique=True)
#     address = db.column(db.String(200))
#     current_popularity = db.column(db.Integer)
#     rating = db.column(db.Integer)

#     def __int__(self, name, address, current_popularity, rating):
#         self.name = name
#         self.address = address
#         self.current_popularity = current_popularity
#         self.rating = rating


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        city = request.form['city']
        # location = request.form['location']
        if city == '':
            return render_template('index.html')
        pop_spots = get_popularity.checkCity(city)
        return render_template('results.html', city=city, spots=pop_spots)


if __name__ == '__main__':
    app.run()
