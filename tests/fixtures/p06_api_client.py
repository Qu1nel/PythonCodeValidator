"""A well-structured API client."""
import requests

API_KEY = "SECRET_KEY_HERE"
BASE_URL = "https://api.weather.com/v1"


def get_weather(city: str) -> dict | None:
    """Fetches weather for a city."""
    try:
        response = requests.get(f"{BASE_URL}/current", params={"q": city, "key": API_KEY})
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
