import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-not-secret")
    YELP_API_KEY = os.environ.get("YELP_API_KEY", "5EwGXrez61sYdXlbdrlyeW6EISyx3DDZ9T0NxHZ5ucimTXzyZ7FTVDVzBMwvhx9S1ZQPrlphoAXjadiZQZp0CahlCy-QoV9IzWrvcSDgk885cCsSNsLLpDJsC1dHX3Yx")
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyDeGaNjFcWO1efbZ4vxnQKcl5-H_6RQeCE")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0")


