# Tipsy Mayflower

Modernized Flask app (2025-ready)

## Setup

1. Create a virtualenv and install deps:

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file with:

```
FLASK_DEBUG=1
SECRET_KEY=dev
YELP_API_KEY=your_yelp_api_key
GOOGLE_MAPS_API_KEY=your_gmaps_key

## Local setup

1. Create a `.env` file with the following variables (see `.env.example`):

```

SECRET_KEY=your_secret
YELP_API_KEY=your_yelp_api_key
GOOGLE_MAPS_API_KEY=your_gmaps_key
FLASK_DEBUG=0

```

2. Never commit real secrets. The `.env` file is ignored by git.
```

3. Run locally:

```
python app.py
```

## Deploy

Set the same env vars on your platform (Heroku/Fly/Render). Dockerfile uses Python 3.12.
