import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    YELP_API_KEY = os.environ.get("YELP_API_KEY")
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0")
