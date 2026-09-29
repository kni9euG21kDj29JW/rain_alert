import os

import requests
from twilio.rest import Client

# Weather API constants
WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = os.environ["OWM_API_KEY"]

# Twilio API constants
TWILIO_ACCT_SID = os.environ["TWILIO_ACCT_SID"]
TWILIO_AUTH_TKN = os.environ["TWILIO_AUTH_TKN"]

# Location constants
EDMONTON = {"lat": 53.5462055, "lon": -113.491241,}
HALIFAX = {"lat": 44.648618, "lon": -63.5859487,}

def weather_codes(location: dict[str, float]) -> list[int]:
    parameters = location | {
        "units": "metric",
        "cnt": 4,
        "appid": WEATHER_API_KEY,
    }

    r = requests.get(url=WEATHER_URL, params=parameters)
    r.raise_for_status()
    return [forecast["weather"][0]["id"] for forecast in r.json()["list"] if forecast["weather"][0]["id"] < 700]

def is_rain_today(location: dict[str, float]) -> bool:
    if weather_codes(location):
        return True
    else:
        return False

def send_sms_notification():
    twilio_client = Client(username=TWILIO_ACCT_SID, password=TWILIO_AUTH_TKN)
    twilio_client.messages.create(
        to="+17802172831",
        from_= "+17372508034",
        body="sms_event_notifications"
    )

if is_rain_today(EDMONTON):
    send_sms_notification()
