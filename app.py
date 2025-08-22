from flask import Flask, jsonify, request, render_template
import get_popularity
import os
from datetime import datetime
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    try:
        return render_template('index.html', year=datetime.now().year)
    except Exception as e:
        print(f"Error in index route: {e}")
        return "Error loading page", 500


@app.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            location = request.form['location']
            # city = request.form['city']
            venue = request.form['venue']

            if location == '':
                return render_template('index.html', year=datetime.utcnow().year)
            if location != '':
                hotSpots, notHopSpots = get_popularity.checkCity(
                    location, venue)
                # Prepare heatmap points from hotspot coordinates
                heatmap_points = []
                for spot in hotSpots:
                    try:
                        lat = spot['lat']
                        lng = spot['lng']
                        weight = spot.get('current_popularity') or 1
                        heatmap_points.append({'lat': lat, 'lng': lng, 'weight': weight})
                    except (KeyError, TypeError):
                        continue
                # Compute a reasonable center
                if heatmap_points:
                    avg_lat = sum(p['lat'] for p in heatmap_points) / len(heatmap_points)
                    avg_lng = sum(p['lng'] for p in heatmap_points) / len(heatmap_points)
                    heatmap_center = {'lat': avg_lat, 'lng': avg_lng}
                else:
                    heatmap_center = {'lat': 40.7128, 'lng': -74.0060}
            # serializedHotSpots = json.dumps(hotSpots)
            # print(hotSpots[0][0]['lat'])
            return render_template(
                'results.html',
                location=location,
                spots=hotSpots,
                notHotSpots=notHopSpots,
                heatmap_points=heatmap_points if location != '' else [],
                heatmap_center=heatmap_center if location != '' else None,
                google_maps_api_key=app.config.get('GOOGLE_MAPS_API_KEY', ''),
                year=datetime.utcnow().year,
            )
    except(IndexError, KeyError, TypeError):
        print('ERROR in call: ')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
