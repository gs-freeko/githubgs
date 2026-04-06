import requests
from config import WEATHER_API_KEY, WEATHER_URL

def fetch_weather(city: str) -> dict:
    """
    Fetch current weather for a given city from OpenWeatherMap API.

    Args:
        city (str): Name of the city e.g. 'Chennai'

    Returns:
        dict: Normalized weather data or error dict
    """
    try:
        params = {
            "q":     city,
            "appid": WEATHER_API_KEY,
            "units": "metric"   # Celsius
        }

        response = requests.get(WEATHER_URL, params=params, timeout=5)
        response.raise_for_status()   # Raises HTTPError for 4xx/5xx
        raw = response.json()

        # ── Normalize: extract only what we need ──
        return {
            "source":      "weather",
            "city":        raw["name"],
            "country":     raw["sys"]["country"],
            "temperature": raw["main"]["temp"],
            "feels_like":  raw["main"]["feels_like"],
            "humidity":    raw["main"]["humidity"],
            "condition":   raw["weather"][0]["description"],
            "wind_speed":  raw["wind"]["speed"],
            "status":      "success"
        }

    except requests.exceptions.Timeout:
        return {"source": "weather", "status": "error", "message": "Request timed out"}

    except requests.exceptions.HTTPError as e:
        return {"source": "weather", "status": "error", "message": str(e)}

    except Exception as e:
        return {"source": "weather", "status": "error", "message": str(e)}
