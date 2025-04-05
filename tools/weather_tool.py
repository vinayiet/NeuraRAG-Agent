import requests 
import os

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f""