# Tipsy Mayflower

Modernized Flask app (2025-ready) with enhanced security, monitoring, and performance features.

## Features

### Core Functionality

- **Location Search**: Find popular venues in any city or neighborhood
- **Venue Types**: Support for bars, lounges, night clubs, and more
- **Heatmap Visualization**: Interactive Google Maps with popularity data
- **Real-time Data**: Uses Google Places API for current popularity information
- **Interactive Loader**: Beautiful loading animation with progress tracking during searches

### Security & Performance

- **Rate Limiting**: 10 requests per minute per IP address
- **Input Validation**: Comprehensive form validation and sanitization
- **CORS Support**: Ready for frontend integration
- **Environment Validation**: Startup checks for required configuration

### Monitoring & Debugging

- **Health Check Endpoint**: `/health` for uptime monitoring
- **Structured Logging**: Comprehensive logging with timestamps
- **Error Handling**: Custom 404 and 500 error pages
- **Input Validation**: Clear error messages for invalid data

## Setup

### Local Development

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:

```bash
SECRET_KEY=your_secret_key
YELP_API_KEY=your_yelp_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
FLASK_DEBUG=1
```

3. Run the application:

```bash
python app.py
```

### Testing

```bash
# Run the test suite
python test_app.py
```

## Deployment

### Heroku

The app is configured for Heroku deployment with:

- Gunicorn WSGI server
- Environment variable configuration
- Procfile for process management

Set environment variables on Heroku:

```bash
heroku config:set GOOGLE_MAPS_API_KEY=your_key
heroku config:set YELP_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret
```

### Docker

```bash
docker build -t tipsy-mayflower .
docker run -p 5000:5000 -e GOOGLE_MAPS_API_KEY=your_key tipsy-mayflower
```

## API Endpoints

- `GET /` - Main search page
- `POST /submit` - Search for venues (rate limited: 10/min)
- `GET /health` - Health check endpoint
- `GET /about` - About page
- `GET /contact` - Contact page

## Environment Variables

| Variable              | Description         | Required |
| --------------------- | ------------------- | -------- |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | Yes      |
| `YELP_API_KEY`        | Yelp API key        | Yes      |
| `SECRET_KEY`          | Flask secret key    | Yes      |
| `FLASK_DEBUG`         | Debug mode (0/1)    | No       |
| `PORT`                | Server port         | No       |

## Security Notes

- Never commit real API keys to version control
- The `.env` file is ignored by git
- Rate limiting prevents API abuse
- Input validation prevents malicious data
- CORS is configured for development (restrict in production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
