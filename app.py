import logging
from flask import Flask, jsonify, request, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import get_popularity
import os
from datetime import datetime
from dotenv import load_dotenv
from config import Config
from typing import Dict, List, Optional, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_COORDINATES = {'lat': 40.7128, 'lng': -74.0060}  # NYC coordinates
MIN_LOCATION_LENGTH = 2
MAX_LOCATION_LENGTH = 100

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Validate required environment variables on startup
def validate_environment():
    """Validate that required environment variables are set."""
    required_vars = ['GOOGLE_MAPS_API_KEY', 'YELP_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not app.config.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        raise EnvironmentError(f"Missing required environment variables: {missing_vars}")
    
    logger.info("Environment validation passed")

def validate_input(location: str, venue: str) -> Tuple[bool, str]:
    """Validate form input data."""
    if not location or not location.strip():
        return False, "Location is required"
    
    if len(location.strip()) < MIN_LOCATION_LENGTH:
        return False, f"Location must be at least {MIN_LOCATION_LENGTH} characters"
    
    if len(location.strip()) > MAX_LOCATION_LENGTH:
        return False, f"Location must be less than {MAX_LOCATION_LENGTH} characters"
    
    # Basic sanitization
    location = location.strip()
    venue = venue.strip() if venue else ""
    
    return True, ""

def process_heatmap_data(hot_spots: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    """Process hotspot data for heatmap visualization."""
    heatmap_points = []
    
    for spot in hot_spots:
        try:
            lat = float(spot.get('lat', 0))
            lng = float(spot.get('lng', 0))
            weight = float(spot.get('current_popularity', 1))
            
            # Validate coordinates
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                heatmap_points.append({'lat': lat, 'lng': lng, 'weight': weight})
            else:
                logger.warning(f"Invalid coordinates for spot: lat={lat}, lng={lng}")
        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Error processing spot data: {e}")
            continue
    
    # Compute center point
    if heatmap_points:
        avg_lat = sum(p['lat'] for p in heatmap_points) / len(heatmap_points)
        avg_lng = sum(p['lng'] for p in heatmap_points) / len(heatmap_points)
        heatmap_center = {'lat': avg_lat, 'lng': avg_lng}
    else:
        heatmap_center = DEFAULT_COORDINATES.copy()
        logger.info("No valid heatmap points, using default coordinates")
    
    return heatmap_points, heatmap_center

@app.errorhandler(404)
def not_found_error(error):
    """Custom 404 error handler."""
    logger.warning(f"404 error: {request.url}")
    return render_template('404.html', year=datetime.now().year), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error handler."""
    logger.error(f"500 error: {error}")
    return render_template('500.html', year=datetime.now().year), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Rate limit exceeded error handler."""
    logger.warning(f"Rate limit exceeded for IP: {get_remote_address()}")
    return render_template('index.html', 
                         year=datetime.now().year,
                         error="Too many requests. Please wait a moment before trying again."), 429

@app.route('/')
def index():
    """Main page route."""
    try:
        logger.info("Index page accessed")
        return render_template('index.html', year=datetime.now().year)
    except Exception as e:
        logger.error(f"Error in index route: {e}", exc_info=True)
        abort(500)

@app.route('/submit', methods=['POST'])
@limiter.limit("10 per minute")
def submit():
    """Handle form submission and return results."""
    try:
        if request.method != 'POST':
            logger.warning(f"Invalid method {request.method} for /submit")
            abort(405)
        
        # Get and validate form data
        location = request.form.get('location', '')
        venue = request.form.get('venue', '')
        
        # Validate input
        is_valid, error_message = validate_input(location, venue)
        if not is_valid:
            logger.warning(f"Invalid input: {error_message}")
            return render_template('index.html', 
                                year=datetime.now().year,
                                error=error_message), 400
        
        logger.info(f"Processing request for location: {location}, venue: {venue}")
        
        # Get popularity data
        try:
            hot_spots, not_hot_spots = get_popularity.checkCity(location, venue)
            logger.info(f"Found {len(hot_spots)} hot spots and {len(not_hot_spots)} not hot spots")
        except Exception as e:
            logger.error(f"Error calling get_popularity.checkCity: {e}", exc_info=True)
            return render_template('index.html', 
                                year=datetime.now().year,
                                error="Unable to fetch location data. Please try again."), 500
        
        # Process heatmap data
        heatmap_points, heatmap_center = process_heatmap_data(hot_spots)
        
        return render_template(
            'results.html',
            location=location,
            spots=hot_spots,
            notHotSpots=not_hot_spots,
            heatmap_points=heatmap_points,
            heatmap_center=heatmap_center,
            google_maps_api_key=app.config.get('GOOGLE_MAPS_API_KEY', ''),
            year=datetime.now().year,
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in submit route: {e}", exc_info=True)
        abort(500)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Basic health check - could be expanded to check database, external APIs, etc.
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

if __name__ == '__main__':
    try:
        # Validate environment before starting
        validate_environment()
        
        # Bind to PORT if defined, otherwise default to 5000
        port = int(os.environ.get('PORT', 5001))
        debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
        
        logger.info(f"Starting Flask app on port {port}, debug={debug_mode}")
        
        # Run without HTTPS for now (geolocation may still work on localhost)
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        exit(1)
